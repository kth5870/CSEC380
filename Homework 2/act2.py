from requestlib import Request

"""
Kayla Hodgson
09/10/2021
CSEC 380 - HW2 Activity 2
"""

HOSTNAME = "csec380-core.csec.rit.edu"
PORT = 82
FLAG = "flag2"

def get_flag():
    request = Request(HOSTNAME, PORT)

    request.post("/getSecure", {"user":"kth5870"})
    token = request.parse_results("token")

    params = {"user": "kth5870", "token": token}
    request.post("/getFlag2", params)

    print("Flag 2 is: %s" % request.parse_results(FLAG))

def main():
    get_flag()

if __name__ == '__main__':
    main()