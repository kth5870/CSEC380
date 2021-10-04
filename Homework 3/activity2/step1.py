from bs4 import BeautifulSoup
from requestlib import Request
import threading
from crawler import Crawler

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

    threads = []
    for i in range(100):
        thread = threading.Thread(target=crawler.crawl_website())
        threads.append(thread)

        thread.start()

    for t in threads:
        try:
            t.join(timeout=10)
        except:
            print("Timeout occurred")
            continue

def main():
    http_request()

if __name__ == '__main__':
    main()