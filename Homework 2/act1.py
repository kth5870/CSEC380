from requestlib import Request
"""
Kayla Hodgson
09/10/2021
CSEC 380 - HW2 Activity 1
"""

HOSTNAME = "csec380-core.csec.rit.edu"
PORT = 82

def get_flag():
    request = Request(HOSTNAME, PORT)

    # simple get request
    request.post("/?user=kth5870")
    flag = request.parse_results("flag1")
    print("Flag 1 is: %s" % flag)

def main():
    get_flag()

if __name__ == '__main__':
    main()