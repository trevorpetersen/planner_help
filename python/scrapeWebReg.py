import utility
import sys
import requests
import json
import csv

from bs4 import BeautifulSoup

def main():

    utility.checkInput(["coursesFile", "outputFile"],[])
    utility.checkCred()

    filename = sys.argv[1]
    outputFilename = sys.argv[2]
    classes = utility.processData(filename, '\t')

    cookie = utility.getCookie()

    courseData = []
    for x in range(0, len(classes)):

        courseName = classes[x]['SUBJ_CODE'].strip()
        courseCode = classes[x]['CRSE_CODE'].rstrip().replace(' ', '+');

        headers = {
        "Cookie": cookie
        }

        formatted = utility.WEBREG_COURSE_DATA.format(courseName, courseCode);
        result = requests.get(formatted, headers=headers)
        data = json.loads(result.content)

        for obj in data:
            courseData.append(obj)

    utility.printData(courseData,outputFilename)


if __name__ == "__main__":
    main()
