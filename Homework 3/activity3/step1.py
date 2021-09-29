from bs4 import BeautifulSoup
from requestlib import Request
import threading
from crawler import Crawler
from list_queue import Queue
import re
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
            # url = urlparse(company[1])
            # print(company[1])
            #
            # tokens = company[1].split("//")
            # if len(url.path) - 1 == -1:
            #     crawler.queue.enqueue(company[1], 0)
            # else:
            #     crawler.queue.enqueue(company[1], len(url.path) - 1)
            LINKS_LIST.append(company[1])

            # if "www" not in url.netloc:
            #     netloc = url.netloc
            #     port = url.scheme
            #     new_url = "www." + netloc
            #     LINKS_LIST.append((new_url, port))
            # else:
            #     LINKS_LIST.append((url.netloc, url.scheme))
    # print(LINKS_LIST)

def http_request():
    read_from_csv("companies.csv")
    # crawler = None
    # crawler = Crawler(LINKS_LIST[1])
    # crawler.crawl_website()
    for link in LINKS_LIST:
        # print("LNK: ", link)
        crawler = Crawler(link)

        crawler.crawl_website()
        # break
        # break
        # url = link[0]
        # scheme = link[1]
        # if scheme == "http":
        #     crawler = Crawler("http://%s" % url, 80)
        # else:
        #     crawler = Crawler("https://%s" % url, 443)
    # crawler.get_urls()
    # crawler.crawl_website()
    # for i in range(100):
    #     thread = threading.Thread(target=crawler.crawl_website())
    #     thread.start()
    #
    # crawler.join()

def main():
    http_request()

if __name__ == '__main__':
    main()