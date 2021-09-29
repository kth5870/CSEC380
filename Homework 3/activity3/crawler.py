from urllib.parse import urlparse

from bs4 import BeautifulSoup
from requestlib import Request
from list_queue import Queue
import re
import os

MAX_DEPTH = 4

class Crawler:
    def __init__(self, url="", port=80):
        self.url = urlparse(url)
        self.hostname = self.url.netloc
        self.visited = set()
        if self.url.scheme == "https":
            self.port = 443
        else:
            self.port = port

        self.links = set()
        self.queue = Queue()

        self.queue.enqueue(self.url.path, len(self.url.path.split("/")) - 1)
        self.queue.get_values()

    def get_urls(self):
        url = ""
        soup = BeautifulSoup(self.request.response, "html.parser")
        for anchor in soup.find_all("a"):
            try:
                url = anchor.get("href")
            except KeyError:
                pass
            if url is not None and "#" not in url and url != "":
                if url[0] == "/":
                    if url[-1] == "/":
                        url = url.rstrip(url[-1])
                        tokens = url.split("/")
                        if not self.check_depth(tokens):
                            self.queue.enqueue(url, len(tokens) - 1)
                    else:
                        tokens = url.split("/")
                        if not self.check_depth(tokens):
                            self.queue.enqueue(url, len(tokens) - 1)
                            self.links.add((url, len(tokens) - 1))
                elif self.hostname in url:
                    url = urlparse(url)

                    path = url.path
                    if path == "":
                        path = "/"

                    tokens = path.split("/")
                    if not self.check_depth(tokens):

                        self.queue.enqueue(url.path, len(tokens) - 1)
                        self.links.add((url.path, len(tokens) - 1))
        # print("links: ", self.links)
        print("links length: ", len(self.links))

    def check_depth(self, url):
        return len(url) > MAX_DEPTH

    def write_to_file(self):
        try:
            os.mkdir("output")
        except FileExistsError:
            pass
        for link in self.links:
            url, depth = link[0], link[1]
            if url != "":
                with open("output/%s_depth_%s.txt" % (self.hostname, depth), "a+") as file:
                    file.write(url + "\n")

    def crawl_website(self):
        while not self.queue.is_empty():
            token = self.queue.dequeue()

            path = token[0]
            self.request = Request(self.hostname, self.port)

            if path not in self.visited:
                self.request.get(path)

                tokens = self.request.response.decode().split("\r\n")
                status_code = int(tokens[0].split(" ")[1])
                print(status_code)

                if status_code >= 301 and status_code < 400:
                    for t in tokens:
                        if "location:" in t.lower():
                            new_url = t.split(" ")[1]
                            url = urlparse(new_url)
                            print(url)
                            uri = url.path
                            print(url.path)

                            self.hostname = url.netloc
                            print(self.hostname)
                            self.port = 443

                            if url.query != "":
                                uri = "%s?%s" % (url.path, url.query)
                                print(uri)

                            self.request = Request(self.hostname, self.port)
                            self.request.get(uri)
                            self.visited.add(uri)
                            self.get_urls()
                            self.request.close_socket()
                            break
                else:
                    self.visited.add(path)
                    self.get_urls()

            print("visited", self.visited)
            print("visited length:", len(self.visited))
            self.request.close_socket()
            self.crawl_website()
        self.write_to_file()
            # if self.url.path != "":
            #     self.request.get(self.url.path)
            # else:
            #     self.request.get()
            #
            #
            #
            # if status_code == 301:
            #     for t in tokens:
            #         if "location:" in t.lower():
            #             new_url = t.split(" ")[1]
            #             # print(new_url)
            #             url = urlparse(new_url)
            #             self.hostname = url.netloc
            #             # print(url)
            #             self.request = Request(self.hostname, 443)
            #             self.request.get(url.path)
            #             self.get_urls()
            #             self.write_to_file()
            #             break
            # else:
            #     self.get_urls()


        # self.get_urls()
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
        #         self.get_urls()
        #     self.request.close_socket()