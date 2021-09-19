from bs4 import BeautifulSoup
from requestlib import Request
import csv

HOSTNAME = "www.rit.edu"
PORT = 443

"""
Parses the HTML returned by the http request
"""
def parse_html(soup):
    context = soup.find_all("tr", {"class": "hidden-row"}, {"class": "course-name"})
    print(context)
    courses = {}
    for i in context:
        if i.contents[0].contents[0] is not None:
            tag = i.contents[0].contents[0].string.strip().split()
            if len(tag) == 1:
                name = i.contents[2].find_all("div", {"class": "course-name"})[0].get_text().strip()
                token = name.split(":")
                if len(token) == 2:
                    courses[str(tag[0])] = token[1].strip()
                else:
                    courses[str(tag[0])] = token[0].strip()
    write_courses_to_csv(courses)

"""
Creates a csv file given the dictionary of the course number of name
"""
def write_courses_to_csv(course):
    with open("classes.csv", "w") as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=["Course #", "Name"],
                                    extrasaction='ignore', lineterminator='\n')
        csv_writer.writeheader()
        for k, v in course.items():
            csv_writer.writerow({csv_writer.fieldnames[0]: k.strip(), csv_writer.fieldnames[1]: v.strip()})
    csv_file.close()

def http_request():
    request = Request(HOSTNAME, PORT)
    response = request.post("/study/computing-security-bs")

    soup = BeautifulSoup(response, "html.parser")
    parse_html(soup)

def main():
    http_request()

if __name__ == '__main__':
    main()