from bs4 import BeautifulSoup
from requestlib import Request
import threading
from list_queue import Queue

HOSTNAME = "www.rit.edu"
PORT = 443
MAX_DEPTH = 4
LINKS = Queue()

"""
Parses the HTML returned by the http request
"""


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
    LINKS.get_values()

def check_depth(url):
    return len(url) > MAX_DEPTH

def crawl_website(queue):
    visited = set()
    while not queue.is_empty():
        request = Request(HOSTNAME, PORT)
        url = queue.dequeue()[0]
        if url not in visited:
            if HOSTNAME in url:
                url = url.replace("https://%s" % HOSTNAME, "")
                request.get(url)
            else:
                request.get(url)
            visited.add(url)
            get_urls(request)
            request.close_socket()

def http_request():
    request = Request(HOSTNAME, PORT)
    request.post("/")

    get_urls(request)
    crawl_website(LINKS)

def main():
    http_request()

if __name__ == '__main__':
    main()