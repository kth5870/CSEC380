import socket, ssl
import json
import urllib.parse as ul

"""
Kayla Hodgson
09/10/2021
CSEC 380 - HW3 Request Library
Creates a POST or GET HTTP Request Header to send to the 
server at port 82 and parses the results of the response sent back
"""

USERAGENT="Mozilla/5.0 (Windows NT 10.0; Trident/7.0; rv:11.0) like Gecko"

class Request:
    def __init__(self, hostname, port=0, user_agent=USERAGENT):
        self.hostname = hostname
        self.port = port
        self.user_agent = user_agent
        self.status_code = 0
        self.location = ""

        context = ssl.SSLContext(ssl.PROTOCOL_TLS)

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.https_socket = context.wrap_socket(self.socket, server_hostname=self.hostname)
        self.https_socket.connect((self.hostname, self.port))

    def request_header(self, request_type, path, data=""):
        header = "%s %s HTTP/1.1\r\n" % (request_type, path)
        header += "Host: %s\r\n" % (self.hostname)
        header += "User-Agent: %s\r\n" % self.user_agent
        header += "Accept: text/html\r\n"
        header += "Accept-Language: en-US\r\n"
        header += "Accept-Encoding: text/html\r\n"

        if request_type == "POST":
            data_str = ul.urlencode(data)
            header += "Connection: keep-alive\r\n"
            header += "Content-Type: application/x-www-form-urlencoded\r\n"
            header += "Content-Length: %i\r\n" % (len(data_str))
            header += "\r\n"
            header += data_str

        header += "Connection: close\r\n"

        # print(header)
        return header

    def get(self, path):
        request = self.request_header("GET", path)
        self.https_socket.sendall(request.encode("utf-8"))

        # self.response = self.https_socket.recv(4096)
        page = self.https_socket.recv(8192)
        while True:
            print(page.decode())
            page = self.https_socket.recv(8192)
            if len(page) != 8192:  # when done receiving data
                break

        print(page)


        # print(self.https_socket.recv(8192))
        # print(self.response.decode())

    def post(self, path, data=""):
        request = self.request_header("POST", path, data)
        self.https_socket.sendall(request.encode())
        # self.response = self.https_socket.recv(4096)

        return self.get_http_content()
        # print(string2)
        # print(self.response.decode())
        # token = self.response.decode()
        # new_location = {}
        #
        # t = token.split("\r\n")
        # self.status_code = int(t[0].split(" ")[1])
        # print(self.status_code)
        # if self.status_code > 300:
        #     for i in t[1:]:
        #         if "Location" in i:
        #             location = i.split(" ")
        #             new_location[location[0].replace(":", "")] = location[1]
        #             break
        #
        # self.location = new_location["Location"]
        # print(self.location)

    def get_http_content(self):
        page = self.https_socket.recv(4096)
        string = ""
        while True:
            # print(page.decode())
            page = self.https_socket.recv(4096)
            string += page.decode()
            if len(page) != 4096:  # when done receiving data
                break

        string2 = ""
        while True:
            # print(page.decode())
            page = self.https_socket.recv(4096)
            string2 += page.decode()
            if len(page) != 4096:  # when done receiving data
                break
        # print(string2)
        return string2

    def parse_results(self, key):
        token = self.response.decode()
        tokens = token.split("\r\n")
        i = 0
        for t in tokens:
            if key in t:
                return json.loads(tokens[i])[key]
            else:
                i += 1