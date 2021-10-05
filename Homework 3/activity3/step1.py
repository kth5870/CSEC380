from bs4 import BeautifulSoup
from requestlib import Request
import threading
from crawler import Crawler
from list_queue import Queue
import threading
import csv
from urllib.parse import urlparse

HOSTNAME = "www.rit.edu"
PORT = 443
MAX_DEPTH = 4
LINKS = Queue()

"""
Parses the HTML returned by the http request
"""

LINKS_LIST = []


def read_from_csv(filename):
    with open(filename) as csv_file:
        reader = csv.reader(csv_file)
        for company in reader:
            LINKS_LIST.append(company[1])

def http_request():
    read_from_csv("companies.csv")

    for link in LINKS_LIST:
        print("creating crawler instance...")
        crawler = Crawler(link)
        crawler.start()
        print("done!")

def main():
    http_request()

if __name__ == '__main__':
    main()