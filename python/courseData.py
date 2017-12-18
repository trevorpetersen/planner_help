import utility

import sys
import requests
import json
import csv

from bs4 import BeautifulSoup

def main():

    utility.checkInput(["coursesFile", "outputFile", "quarterCode"],[])
    utility.checkCred()

    filename = sys.argv[1]
    outputFilename = sys.argv[2]
    quarterCode = sys.argv[3]

    courses = utility.processData(filename, '\t')

    cookie = utility.getCookie()

    utility.checkQuarterCode(quarterCode, cookie)

    scrapeWebReg(courses, outputFilename, quarterCode, cookie)

def scrapeWebReg(courses, outputFilename, quarterCode, cookie):
    courseData = getCourseData(courses, quarterCode, cookie)
    utility.printData(courseData, outputFilename)


def getCourseData(courses, quarterCode, cookie):
    courseData = []
    for x in range(0, len(courses)):

        courseName = courses[x]['SUBJ_CODE'].strip()
        courseCode = courses[x]['CRSE_CODE'].rstrip().replace(' ', '+');

        utility.updateStatus("Getting course data for " + courseName + " " + courses[x]['CRSE_CODE'].strip())

        headers = {
        "Cookie": cookie
        }

        formatted = utility.WEBREG_COURSE_DATA.format(courseName, courseCode, quarterCode);
        result = requests.get(formatted, headers=headers)
        data = json.loads(result.content)

        for obj in data:
            courseData.append(obj)

    sys.stdout.write('\n')
    return courseData


if __name__ == "__main__":
    main()
