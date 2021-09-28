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
            url = urlparse(company[1])
            LINKS_LIST.append(company[1])

            # if "www" not in url.netloc:
            #     netloc = url.netloc
            #     port = url.scheme
            #     new_url = "www." + netloc
            #     LINKS_LIST.append((new_url, port))
            # else:
            #     LINKS_LIST.append((url.netloc, url.scheme))
    print(LINKS_LIST)




def get_urls(request):
    url = ""
    soup = BeautifulSoup(request.response, "html.parser")
    for anchor in soup.find_all("a"):
        try:
            url = anchor.get("href")
        except KeyError:
            pass
        if url is not None and "#" not in url and url != "":
            if url[0] == "/":
                tokens = url.split("/")
                if not check_depth(tokens):
                    LINKS.enqueue(url, len(tokens)-1)
            elif HOSTNAME in url:
                link = url.replace("https://%s" % HOSTNAME, "")
                tokens = link.split("/")
                if not check_depth(tokens):
                    LINKS.enqueue(url, len(tokens)-1)

def check_depth(url):
    return len(url) > MAX_DEPTH

# def get_emails(request, depth):
#     email = re.findall(r'[a-zA-Z0-9\.\-\_,]+\@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,24}', request.response.decode())
#     for i in set(email):
#         write_to_file(i, depth)

def write_to_file(email, depth):
    with open("depth_%s.txt" % depth, "a+") as file:
        if email not in file:
            file.write(email+"\n")
    file.close()

def crawl_website(queue):
    visited = set()
    while not queue.is_empty():
        token = queue.dequeue()
        url = token[0]
        depth = token[1]
        request = Request(url, PORT)
        if url not in visited:
            if HOSTNAME in url:
                url = url.replace("https://%s" % HOSTNAME, "")
                request.get(url)
            else:
                request.get(url)
            visited.add(url)


def http_request():
    read_from_csv("companies.csv")

    crawler = None
    crawler = Crawler(LINKS_LIST[1])
    crawler.crawl_website()
    # for link in LINKS_LIST:
    #     crawler = Crawler(link)
    #     url = link[0]
    #     scheme = link[1]
    #     if scheme == "http":
    #         crawler = Crawler("http://%s" % url, 80)
    #     else:
    #         crawler = Crawler("https://%s" % url, 443)
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