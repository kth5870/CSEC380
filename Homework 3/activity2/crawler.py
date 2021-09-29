from bs4 import BeautifulSoup
from requestlib import Request
from list_queue import Queue
import re

MAX_DEPTH = 4

class Crawler:
    def __init__(self, request):
        self.request = request
        self.hostname = request.hostname
        self.port = request.port
        self.queue = Queue()

    def get_urls(self):
        url = ""
        soup = BeautifulSoup(self.request.response, "html.parser")
        for anchor in soup.find_all("a"):
            try:
                url = anchor.get("href")
            except KeyError:
                pass
            if url is not None and "#" not in url and url != "":
                if url[-1] == "/":
                    url = url.rstrip((url[-1]))
                elif url[0] == "/":
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

    def get_emails(self, depth):
        email = re.findall(r'[a-zA-Z0-9\.\-\_,]+\@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,24}', self.request.response.decode())
        for i in set(email):
            self.write_to_file(i, depth)

    def write_to_file(self, email, depth):
        with open("depth_%s.txt" % depth, "a+") as file:
            file.write(email + "\n")
            print("wrote to depth_%s.txt" % depth)

    def crawl_website(self):
        visited = set()
        while not self.queue.is_empty():
            self.request = Request(self.hostname, self.port)
            token = self.queue.dequeue()
            print(token)
            url = token[0]
            depth = token[1]
            if url not in visited:
                if self.hostname in url:
                    url = url.replace("https://%s" % self.hostname, "")
                    self.request.get(url)
                else:
                    self.request.get(url)
                visited.add(url)
                self.get_emails(depth)
                self.get_urls()
            self.request.close_socket()