from bs4 import BeautifulSoup
import requestlib

class Crawler:
    def __init__(self, hostname):
        self.hostname = hostname

    def get_urls(self, url):
        pass

    def parse_html(self, request):
        links = []
        soup = BeautifulSoup(request.response)
        for i in soup.find_all("a"):
            url = i.get("href")
            if url is not None and "#" not in url and url != "":
                if url[0] == "/":
                    tokens = url.split("/")
                    depth_bool = self.check_depth(tokens)
                    if depth_bool:
                        links.append(i)
                elif self.hostname in url:
                    tokens = url.replace("https://%s" % self.hostname, "").split("/")
                    depth_bool = self.check_depth(tokens)
                    if not depth_bool:
                        links.append(i)
                        # print(tokens)

    def check_depth(self, url, depth=4):
        return len(url) > depth
