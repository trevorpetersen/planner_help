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
    courses = utility.processData(filename, '\t')

    cookie = utility.getCookie()

    scrapeWebReg(courses, outputFilename, cookie)

def scrapeWebReg(courses, outputFilename, cookie):
    courseData = getCourseData(courses, cookie)
    utility.printData(courseData, outputFilename)


def getCourseData(courses, cookie):
    courseData = []
    for x in range(0, len(courses)):

        courseName = courses[x]['SUBJ_CODE'].strip()
        courseCode = courses[x]['CRSE_CODE'].rstrip().replace(' ', '+');

        utility.updateStatus("Getting course data for " + courseName + " " + courses[x]['CRSE_CODE'].strip())

        headers = {
        "Cookie": cookie
        }

        formatted = utility.WEBREG_COURSE_DATA.format(courseName, courseCode);
        result = requests.get(formatted, headers=headers)
        data = json.loads(result.content)

        for obj in data:
            courseData.append(obj)

    sys.stdout.write('\n')
    return courseData


if __name__ == "__main__":
    main()
