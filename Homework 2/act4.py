from requestlib import Request

"""
Kayla Hodgson
09/10/2021
CSEC 380 - HW2 Activity 1
"""

HOSTNAME = "csec380-core.csec.rit.edu"
PORT = 82
FLAG = "flag4"

def get_flag():
    request = Request(HOSTNAME, PORT)

    request.post("/getSecure", {"user":"kth5870"})
    token = request.parse_results("token")

    params = {"user":"kth5870", "token": token, "username": "kth5870"}
    request.post("/createAccount", params)
    password = request.parse_results("account_password")

    params = {"user":"kth5870", "token": token, "username": "kth5870", "password": password}
    request.post("/login", params)

    print("Flag 4 is: %s" % request.parse_results(FLAG))

def main():
    get_flag()

if __name__ == '__main__':
    main()