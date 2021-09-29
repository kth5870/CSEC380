from bs4 import BeautifulSoup
from requestlib import Request
from multiprocessing.dummy import Pool
import os
import shutil

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
    with open("images/%s" % name, "wb") as folder:
        folder.write(request.response)

def get_image_name(img):
    tokens = img.split("/")

    if "&" in tokens[-1]:
        t = tokens[-1].split("=")
        photo_name = t[2].split("&")
        return photo_name[0]+".jpg"

    return tokens[-1]

def download_images(img):
        name = get_image_name(img)

        if img[0] == "/":
            request = Request("www.rit.edu", 443)
            request.get(img)

            write_image_to_folder(name, request)
        else:
            request = Request("claws.rit.edu", 443)
            token = img.split("/")
            request.get("/photos/" + token[-1])

            write_image_to_folder(name, request)

def http_request():
    request = Request(HOSTNAME, PORT)
    request.post("/computing/directory?term_node_tid_depth=4919")

    soup = BeautifulSoup(request.response, "html.parser")
    images = parse_html(soup)

    try:
        os.mkdir("images")
    except FileExistsError:
        shutil.rmtree("images")
        os.mkdir("images")

    pool = Pool(30)
    print("downloading images... ")
    pool.map(download_images, images)
    print("done!")
    pool.close()
    pool.join()

def main():
    http_request()

if __name__ == '__main__':
    main()