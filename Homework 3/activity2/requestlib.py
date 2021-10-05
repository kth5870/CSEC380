import socket, ssl
import json
import urllib.parse as ul

"""
Kayla Hodgson
09/10/2021
CSEC 380 - HW3 Request Library
Creates a POST or GET HTTP Request Header to send to the 
server and parses the results of the response sent back
"""

USERAGENT="Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5 (.NET CLR 3.5.30729)"

class Request:
    def __init__(self, hostname, port=0, user_agent=USERAGENT):
        self.hostname = hostname
        self.port = port
        self.user_agent = user_agent
        self.status_code = 0

        try:
            context = ssl.SSLContext(ssl.PROTOCOL_TLS)
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.https_socket = context.wrap_socket(self.socket, server_hostname=self.hostname)
            self.https_socket.connect((self.hostname, self.port))
            self.https_socket.settimeout(5)
        except socket.gaierror:
            print("Error creating socket")
            pass

    def request_header(self, request_type, path, data=""):
        header = "%s %s HTTP/1.1\r\n" % (request_type, path)
        header += "Host: %s\r\n" % (self.hostname)
        header += "User-Agent: %s\r\n" % self.user_agent
        header += "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/jpeg,*/*;q=0.8\r\n"
        header += "Accept-Language: en-US\r\n"

        if request_type == "POST":
            data_str = ul.urlencode(data)
            header += "Content-Type: application/x-www-form-urlencoded\r\n"
            header += "Content-Length: %i\r\n" % (len(data_str))
            header += "\r\n"
            header += data_str

        header += "Connection: keep-alive\r\n"
        header += "\r\n"
        return header

    def get(self, path):
        request = self.request_header("GET", path)
        self.https_socket.sendall(request.encode())
        self.response = b''

        try:
            self.response += self.https_socket.recv(4096)

            tokens = self.response.decode().split("\r\n")
            status_code = int(tokens[0].split(" ")[1])

            if status_code == 404:
                print(self.response)
            elif status_code >= 301 and status_code <= 404:
                pass
            else:
                while True:
                    page = self.https_socket.recv(4096 * 360)
                    self.response += page

                    if b'</html>' in self.response:
                        break
        except socket.timeout:
            print("Timed out on page %s" % path)

        return self.response

    def post(self, path, data=""):
        request = self.request_header("POST", path, data)
        self.https_socket.sendall(request.encode())

        self.get_http_content()
        return self.response

    def get_http_content(self):
        self.response = self.https_socket.recv(4096 * 360)

        while True:
            page = self.https_socket.recv(4096 * 360)
            if len(page) != 4096:
                break

        self.recv_data(2)

    def recv_data(self, number):
        self.response = self.https_socket.recv(4096 * 360)

        while number > 0:
            while True:
                page = self.https_socket.recv(4096 * 360)
                self.response += page
                if len(page) != 4096 * 360:  # when done receiving data
                    break
            number -= 1

    def parse_results(self, key):
        token = self.response.decode()
        tokens = token.split("\r\n")
        i = 0
        for t in tokens:
            if key in t:
                return json.loads(tokens[i])[key]
            else:
                i += 1

    def close_socket(self):
        self.https_socket.close()