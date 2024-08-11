# Subdomain Enumeration Script

This Python script is designed to discover subdomains for a given target URL by using a wordlist. It sends HTTP requests to potential subdomains and checks if they are valid by analyzing the response status code.

## Features

- **Simple to Use**: Just provide a target URL, and the script does the rest.
- **Efficient**: Sends HTTP requests and checks for valid subdomains.
- **Customizable**: You can use your own wordlist for subdomain enumeration.

## Requirements

- Python 3.x
- `requests` library

## Installation

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/Cyber-30/Subdomain-Enumeration.git
    cd Subdomain-Enumeration
    ```

2. **Install Dependencies**:
    ```bash
    pip install requests
    ```

3. **Prepare Your Wordlist**:
    - Ensure you have a `subdomainwordlist.txt` file in the same directory as the script. This file should contain potential subdomains, one per line.

## Example Output

Here’s an example of the script discovering subdomains:

![Subdomain Discovery](images/output.png)

## Usage

Run the script with the following command:

```bash
python script.py <target_url>
