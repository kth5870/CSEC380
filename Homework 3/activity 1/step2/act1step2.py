from bs4 import BeautifulSoup
from requestlib import Request
import os
import requests
import shutil
import sys

HOSTNAME = "www.rit.edu"
PORT = 443

"""
Parses the HTML returned by the http request
"""
def parse_html(soup):
    images = []
    context = soup.find_all("img")
    for i in context:
        try:
            images.append(i["data-src"])
        except KeyError:
            images.append(i["src"])
    return images

def write_image_to_folder(name, request):
    print(request.response)
    # print(request.response.split(b'\r\n\r\n')[1])
    with open("images/%s" % name, "wb") as folder:
                folder.write(request.response)

def get_image_name(img):
    tokens = img.split("/")

    if "&" in tokens[-1]:
        t = tokens[-1].split("=")
        photo_name = t[2].split("&")
        return photo_name[0]+".jpg"

    return tokens[-1]

def download_images(images):
    # os.mkdir("images")
    for img in images:
        name = get_image_name(img)
        if img[0] == "/":
            request = Request("www.rit.edu", 443)
            print("downloading image", img)
            request.get(img)

            write_image_to_folder(name, request)
            # print(request.response.split(b'\r\n\r\n')[1])
        else:
            request = Request("claws.rit.edu", 443)
            token = img.split("/")
            print("downloading image", token[-1])
            request.get("/photos/" + token[-1])

            write_image_to_folder(name, request)

def http_request():
    request = Request(HOSTNAME, PORT)
    request.post("/computing/directory?term_node_tid_depth=4919")

    soup = BeautifulSoup(request.response, "html.parser")
    images = parse_html(soup)
    download_images(images)

def main():
    http_request()

if __name__ == '__main__':
    main()