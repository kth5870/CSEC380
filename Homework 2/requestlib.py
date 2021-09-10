import socket
import json
import urllib.parse as ul

"""
Kayla Hodgson
09/10/2021
CSEC 380 - HW2 Request Library
Creates a POST or GET HTTP Request Header to send to the 
server at port 82 and parses the results of the response sent back
"""

USERAGENT="Mozilla/5.0 (Windows NT 10.0; Trident/7.0; rv:11.0) like Gecko"

class Request:
    def __init__(self, hostname, port, user_agent=USERAGENT):
        self.hostname = hostname
        self.port = port
        self.user_agent = user_agent

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.hostname, self.port))


    def request_header(self, request_type, path, data=""):
        data_str = ul.urlencode(data)

        header = "%s %s HTTP/1.1\r\n" % (request_type, path)
        header += "Host: %s:%s\r\n" % (self.hostname, self.port)
        header += "User-Agent: %s\r\n" % self.user_agent
        header += "Accept: text/html\r\n"
        header += "Accept-Language: en-US\r\n"
        header += "Accept-Encoding: text/html\r\n"
        header += "Content-Type: application/x-www-form-urlencoded\r\n"
        header += "Connection: keep-alive\r\n"
        header += "Content-Length: %i\r\n" % (len(data_str))
        header += "\r\n"
        header += data_str

        return header

    def get(self, path):
        request = self.request_header("GET", path)
        self.socket.sendall(request.encode("utf-8"))
        self.response = self.socket.recv(4096)

    def post(self, path, data=""):
        request = self.request_header("POST", path, data)
        self.socket.sendall(request.encode("utf-8"))
        self.response = self.socket.recv(4096)

    def parse_results(self, key):
        token = self.response.decode()
        tokens = token.split("\r\n")
        i = 0
        for t in tokens:
            if key in t:
                return json.loads(tokens[i])[key]
            else:
                i += 1