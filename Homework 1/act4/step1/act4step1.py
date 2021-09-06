import requests
"""
Kayla Hodgson
CSEC 380 - Homework 1
Step 1 Act 4
09/03/2021
"""

def request_url():
    request = requests.get("https://csec.rit.edu")

def main():
    request_url()

if __name__ == "__main__":
    main()