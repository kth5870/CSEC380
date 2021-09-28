from urllib.parse import urlparse

from bs4 import BeautifulSoup
from requestlib import Request
from list_queue import Queue
import re
import csv

MAX_DEPTH = 4

class Crawler:
    def __init__(self, url, port=80):
        self.url = urlparse(url)
        self.hostname = self.url.netloc
        if self.url.scheme == "https":
            self.port = 443
        else:
            self.port = port
        self.links = []
        self.queue = Queue()
        # self.request = Request(self.hostname, self.port)


    def get_urls(self):
        url = ""
        soup = BeautifulSoup(self.request.response, "html.parser")
        for anchor in soup.find_all("a"):
            try:
                url = anchor.get("href")
            except KeyError:
                pass
            if url is not None and url != "":
                if url[0] == "/":
                    tokens = url.split("/")
                    if not self.check_depth(tokens):
                        self.queue.enqueue(url, len(tokens) - 1)
                elif self.hostname in url:
                    link = url.replace("https://%s" % self.hostname, "")
                    tokens = link.split("/")
                    if not self.check_depth(tokens):
                        self.queue.enqueue(url, len(tokens) - 1)

    def check_depth(self, url):
        return len(url) > MAX_DEPTH

    # def get_emails(self, depth):
    #     email = re.findall(r'[a-zA-Z0-9\.\-\_,]+\@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,24}', self.request.response.decode())
    #     for _ in set(email):
    #         self.write_to_file(depth)

    def write_to_file(self, depth):
        with open("depth_%s.txt" % depth, "a+") as file:
            if self.url.netloc not in file:
                file.write(self.url.netloc + "\n")
        file.close()

    def crawl_website(self):
        visited = set()
        self.request = Request(self.hostname, self.port)
        if self.url.path != "":
            self.request.get(self.url.path)
        else:
            self.request.get()
        self.get_urls()
        # while not self.queue.is_empty():
        #     self.request = Request(self.hostname, self.port)
        #     token = self.queue.dequeue()
        #     print(token)
        #     url = token[0]
        #     depth = token[1]
        #     if url not in visited:
        #         if self.hostname in url:
        #             url = url.replace("https://%s" % self.hostname, "")
        #             self.request.get(url)
        #         else:
        #             self.request.get(url)
        #         visited.add(url)
        #     self.request.close_socket()