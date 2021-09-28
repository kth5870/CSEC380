from bs4 import BeautifulSoup
from requestlib import Request
import threading
from crawler import Crawler
from list_queue import Queue
import re

HOSTNAME = "www.rit.edu"
PORT = 443

"""
Parses the HTML returned by the http request
"""

def http_request():
    request = Request(HOSTNAME, PORT)
    request.post("/")

    crawler = Crawler(request)
    crawler.get_urls()

    for i in range(100):
        thread = threading.Thread(target=crawler.crawl_website())
        thread.start()

    crawler.join()


def main():
    http_request()

if __name__ == '__main__':
    main()