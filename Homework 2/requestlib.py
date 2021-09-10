import socket

def __init__(self, hostname, port):
    self.hostname = hostname
    self.port = port

    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.socket.connect((self.hostname, self.port))


def request_header(self, request_type, path):
    header = "%s %s HTTP/1.1\r\n" % (request_type, path)
    header += "Host: %s:%s\r\n" % (self.hostname, self.port)
    header += "User-Agent: %s\r\n" % self.useragent
    header += "Accept: text/html\r\n"
    header += "Accept-Language: en-US\r\n"
    header += "Accept-Encoding: text/html\r\n"
    header += "Content-Type: text/html\r\n"
    header += "Connection: keep-alive\r\n"
    # header += "Content-Length: {}\r\n".format(len(data))
    header += "\r\n"
    return header

def get(self, path):
    request = self.request_header("GET", path)
    self.socket.sendall(request.encode("utf-8"))
    self.response = self.socket.recv(4096)

def post(self, path):
    request = self.request_header("POST", path)
    self.socket.sendall(request.encode("utf-8"))
    self.response = self.socket.recv(4096)

def parse_results(self, key):
    token = self.response.decode()
    tokens = token.split("\r\n")
    print(tokens)