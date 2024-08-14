import requests
import sys
import threading
from queue import Queue


class SubdomainFinder:
    def __init__(self, target_url, wordlist_file, output_file=None):
        self.target_url = target_url
        self.wordlist_file = wordlist_file
        self.output_file = output_file
        self.queue = Queue()
        self.discovered_subdomains = []

    def request(self, url):
        """Sends a GET request and returns True if status code is 200, otherwise False."""
        try:
            response = requests.get("https://" + url, timeout=5)
            return response.status_code == 200
        except (requests.exceptions.RequestException, ConnectionError, TimeoutError):
            return False

    def worker(self):
        """Thread worker function that processes the queue."""
        while not self.queue.empty():
            subdomain = self.queue.get()
            test_url = f"{subdomain}.{self.target_url}"
            if self.request(test_url):
                print(f"[+] Subdomain discovered -----> {test_url}")
                self.discovered_subdomains.append(test_url)
            self.queue.task_done()

    def run(self, num_threads=10):
        """Starts the subdomain discovery process."""
        try:
            with open(self.wordlist_file, "r") as wordlist:
                for line in wordlist:
                    self.queue.put(line.strip())

            threads = []
            for _ in range(num_threads):
                thread = threading.Thread(target=self.worker)
                thread.start()
                threads.append(thread)

            for thread in threads:
                thread.join()

            if self.output_file:
                self.save_results()

        except FileNotFoundError:
            print("[-] Subdomain wordlist file not found.")
        except Exception as e:
            print(f"[-] An unexpected error occurred: {e}")

    def save_results(self):
        """Saves the discovered subdomains to a file."""
        try:
            with open(self.output_file, "w") as f:
                for subdomain in self.discovered_subdomains:
                    f.write(subdomain + "\n")
            print(f"[+] Results saved to {self.output_file}")
        except Exception as e:
            print(f"[-] Could not save results: {e}")


def main():
    """Main function to handle command-line arguments and start the subdomain finder."""
    if len(sys.argv) < 3:
        print("Usage: python script.py <target_url> <wordlist_file> [output_file]")
        sys.exit(1)

    target_url = sys.argv[1]
    wordlist_file = sys.argv[2]
    output_file = sys.argv[3] if len(sys.argv) > 3 else None

    finder = SubdomainFinder(target_url, wordlist_file, output_file)
    finder.run()


if __name__ == "__main__":
    main()
