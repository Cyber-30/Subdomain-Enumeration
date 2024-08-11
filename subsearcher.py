import requests
import sys


def request(url):
    """Sends a GET request and returns True if status code is 200, otherwise False."""
    try:
        response = requests.get("https://" + url, timeout=5)
        return response.status_code == 200
    except (requests.exceptions.RequestException, ConnectionError, TimeoutError):
        return False


def main():
    """Main function to handle command-line arguments and subdomain discovery."""
    if len(sys.argv) != 2:
        print("Usage: python script.py <target_url>")
        sys.exit(1)

    target_url = sys.argv[1]

    try:
        with open("subdomainwordlist.txt", "r") as wordlist:
            for line in wordlist:
                word = line.strip()
                test_url = word + "." + target_url
                if request(test_url):
                    print("[+] Subdomain discovered -----> " + test_url)
    except FileNotFoundError:
        print("[-] Subdomain wordlist file not found.")
    except Exception as e:
        print(f"[-] An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
