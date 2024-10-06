# Subsearcher Script

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
    git clone https://github.com/Cyber-30/Subsearcher.git
    cd Subsearcher
    ```

2. **Install Dependencies**:
    ```bash
    pip3 install -r requirements.txt
    ```


3. **Prepare Your Wordlist**:
    - Ensure you have a `subdomainwordlist.txt` file in the same directory as the script. This file should contain potential subdomains, one per line.

## Usage

Run the script with the following command:

```bash
python script.py <target_url> <subdomain_wordlist> <output_file>

```

## Example Output

Here’s an example of the script discovering subdomains:

![Screenshot 2024-08-14 215047](https://github.com/user-attachments/assets/cb7aa951-7b9c-4598-bbf1-fe44ef6c9d9b)

