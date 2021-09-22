from bs4 import BeautifulSoup
from requestlib import Request
from list_queue import Queue

MAX_DEPTH = 4

class Crawler:
    def __init__(self, hostname, port):
        self.hostname = hostname
        self.port = port
        self.request = None
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
                if url[0] == "/":
                    tokens = url.split("/")
                    if not self.check_depth(tokens):
                        self.queue.enqueue(url, len(tokens) - 1)
                elif self.hostname in url:
                    link = url.replace("https://%s" % self.hostname, "")
                    tokens = link.split("/")
                    if not self.check_depth(tokens):
                        self.queue.enqueue(url, len(tokens) - 1)
        self.queue.get_values()

    def check_depth(self, url):
        return len(url) > MAX_DEPTH

    """
    BFS algorithm:
    Initialize queue (Q) with initial set of known URL's.
    Until Q is empty (or page or time limit exhausted)
    Pop URL from front of Q.
    If URL is not to be visited
          e.g. it is a .gif, .jpeg, .ps, .pdf etc.,
          or is already visited
          go to top of loop.
          continue loop (get next url).
    Else Download PAGE
    [Index PAGE and/or store cached copy]
    Parse P to obtain list of new links
    Append these links to the end of Q.
    """

    def crawl_website(self):
        visited = set()
        while not self.queue.is_empty():
            self.request = Request(self.hostname, self.port)
            url = self.queue.dequeue()[0]
            if url not in visited:
                if self.hostname in url:
                    url = url.replace("https://%s" % self.hostname, "")
                    self.request.get(url)
                else:
                    self.request.get(url)
                visited.add(url)
                self.get_urls()
                self.request.close_socket()

        # while not self.queue.is_empty():
        #     url = self.queue.dequeue()[0]
        #     if self.hostname in url:
        #         url = url.replace("https://%s" % self.hostname, "")
        #         self.request.get(url)
        #     else:
        #         self.request.get(url)
        #     self.get_urls()




        # for url in list(links):
        #     # depth = url[i](1)
        #     response = self.request.get(url[i][0])
        #     new_links = self.get_urls()
        #     self.crawl_website(new_links)


    # def crawl_website(self, start_url, depth=0):
    #     searched_urls = []
    #
    #     links = [start_url]
    #     if depth < MAX_DEPTH:
    #         for link in links:
    #             if link not in searched_urls:
    #                 searched_urls.append(link)