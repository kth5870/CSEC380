from urllib.parse import urlparse

from bs4 import BeautifulSoup
from requestlib import Request
from list_queue import Queue
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
        print("getting new urls...")
        url = ""
        soup = BeautifulSoup(self.request.response, "html.parser")
        for anchor in soup.find_all("a"):
            try:
                url = anchor.get("href")
            except KeyError:
                pass
            if url is not None and "#" not in url and url != "":
                if url[0] == "/":
                    if url[-1] == "/" and len(url) != 1:
                        url = url.rstrip(url[-1])
                        tokens = url.split("/")
                        if not self.check_depth(tokens):
                            tuple = (url, len(tokens) - 1)
                            self.queue.enqueue(url, len(tokens) - 1)
                            if tuple not in self.links:
                                self.links.add(tuple)
                    else:
                        tokens = url.split("/")
                        if not self.check_depth(tokens):
                            tuple = (url, len(tokens) - 1)
                            self.queue.enqueue(url, len(tokens) - 1)
                            if tuple not in self.links:
                                self.links.add(tuple)
                elif self.hostname in url:
                    uri = urlparse(url)
                    path = uri.path
                    if path == "":
                        path = "/"

                    tokens = path.split("/")
                    if not self.check_depth(tokens):
                        tuple = (path, len(tokens) - 1)
                        self.queue.enqueue(path, len(tokens) - 1)
                        if tuple not in self.links:
                            self.links.add(tuple)
        # print("links length: ", len(self.links))
        print("done!")

    def check_depth(self, url):
        return len(url) > MAX_DEPTH

    def write_to_file(self):
        try:
            os.mkdir("output")
        except FileExistsError:
            pass
        print("writing links to file...")
        for link in self.links:
            url, depth = link[0], link[1]
            if url != "":
                with open("output/%s_depth_%s.txt" % (self.hostname, depth), "a+") as file:
                    file.write(url + "\n")
        print("done!")

    def crawl_website(self):
        print("crawl_website...")
        while not self.queue.is_empty():
            token = self.queue.dequeue()

            path = token[0]
            self.request = Request(self.hostname, self.port)
            # print(path)
            if path not in self.visited:
                self.request.get(path)

                tokens = self.request.response.decode().split("\r\n")
                status_code = int(tokens[0].split(" ")[1])
                # print("crawler", status_code)
                if status_code != 404:
                    if status_code >= 301 and status_code < 400:
                        for t in tokens:
                            # print(tokens)
                            if "location:" in t.lower():
                                new_url = t.split(" ")[1]
                                url = urlparse(new_url)
                                # print(url)
                                uri = url.path
                                # print(url.path)

                                if url.netloc != "":
                                    self.hostname = url.netloc
                                    # print(self.hostname)
                                    self.port = 443

                                if url.query != "":
                                    uri = "%s?%s" % (url.path, url.query)
                                    # print(uri)

                                self.request = Request(self.hostname, self.port)
                                self.request.get(uri)
                                self.visited.add(uri)
                                self.get_urls()
                                self.request.close_socket()
                                break
                    else:
                        self.visited.add(path)
                        self.get_urls()
        print("done!")
        self.write_to_file()
            # print("visited length:", len(self.visited))
            # print("queue length: ", self.queue.get_size())

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