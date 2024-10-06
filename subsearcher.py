import requests
import threading
from queue import Queue
import logging
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from tqdm import tqdm

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SubdomainFinder:
    def __init__(self, target_url, wordlist_file, output_file=None, num_threads=10):
        self.target_url = target_url
        self.wordlist_file = wordlist_file
        self.output_file = output_file
        self.num_threads = num_threads
        self.queue = Queue()
        self.discovered_subdomains = []

    def request(self, url):
        """Sends a GET request and returns True if status code is 200, otherwise False."""
        try:
            response = requests.get(f"https://{url}", timeout=5)
            return response.status_code == 200
        except requests.exceptions.RequestException as e:
            logging.debug(f"Request failed: {e}")
            return False

    def worker(self):
        """Thread worker function that processes the queue."""
        while not self.queue.empty():
            subdomain = self.queue.get()
            test_url = f"{subdomain}.{self.target_url}"
            if self.request(test_url):
                self.discovered_subdomains.append(test_url)
                self.update_output(f"[+] Subdomain discovered: {test_url}")
            self.queue.task_done()

    def run(self):
        """Starts the subdomain discovery process."""
        try:
            with open(self.wordlist_file, "r") as wordlist:
                subdomains = [line.strip() for line in wordlist]
            
            # Fill the queue with subdomains
            for subdomain in subdomains:
                self.queue.put(subdomain)

            # Create and start threads
            threads = []
            for _ in range(self.num_threads):
                thread = threading.Thread(target=self.worker)
                thread.start()
                threads.append(thread)

            # Wait for threads to finish
            self.queue.join()

            if self.output_file:
                self.save_results()

        except FileNotFoundError:
            messagebox.showerror("Error", "Subdomain wordlist file not found.")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    def update_output(self, message):
        """Updates the output text box with a new message."""
        self.output_box.insert(tk.END, message + "\n")
        self.output_box.see(tk.END)

    def save_results(self):
        """Saves the discovered subdomains to a file."""
        try:
            with open(self.output_file, "w") as f:
                for subdomain in self.discovered_subdomains:
                    f.write(subdomain + "\n")
            messagebox.showinfo("Success", f"Results saved to {self.output_file}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save results: {e}")

class App:
    def __init__(self, master):
        self.master = master
        master.title("Subdomain Finder")

        # Create UI elements
        self.label1 = tk.Label(master, text="Target URL:")
        self.label1.pack()

        self.target_url_entry = tk.Entry(master, width=50)
        self.target_url_entry.pack()

        self.label2 = tk.Label(master, text="Wordlist File:")
        self.label2.pack()

        self.wordlist_file_entry = tk.Entry(master, width=50)
        self.wordlist_file_entry.pack()

        self.browse_button = tk.Button(master, text="Browse", command=self.browse_file)
        self.browse_button.pack()

        self.label3 = tk.Label(master, text="Output File (optional):")
        self.label3.pack()

        self.output_file_entry = tk.Entry(master, width=50)
        self.output_file_entry.pack()

        self.label4 = tk.Label(master, text="Number of Threads:")
        self.label4.pack()

        self.threads_entry = tk.Entry(master, width=5)
        self.threads_entry.insert(0, "10")  # Default value
        self.threads_entry.pack()

        self.start_button = tk.Button(master, text="Start", command=self.start)
        self.start_button.pack()

        self.output_box = scrolledtext.ScrolledText(master, width=60, height=20)
        self.output_box.pack()

    def browse_file(self):
        """Opens a file dialog to select a wordlist file."""
        filename = filedialog.askopenfilename()
        self.wordlist_file_entry.delete(0, tk.END)
        self.wordlist_file_entry.insert(0, filename)

    def start(self):
        """Starts the subdomain finder process."""
        target_url = self.target_url_entry.get()
        wordlist_file = self.wordlist_file_entry.get()
        output_file = self.output_file_entry.get() or None
        num_threads = int(self.threads_entry.get())

        if not target_url or not wordlist_file:
            messagebox.showerror("Input Error", "Please provide both the target URL and wordlist file.")
            return

        finder = SubdomainFinder(target_url, wordlist_file, output_file, num_threads)
        threading.Thread(target=finder.run).start()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
