import utility
import sys
import requests
import json
import csv
from bs4 import BeautifulSoup

def main():
    utility.checkInput(4, ["departments", "ouputFile", "QuarterCode", "WebRegCookie"])
    departmentsFileName = sys.argv[1]
    outputFileName = sys.argv[2]
    quarterCode = sys.argv[3]
    cookie = sys.argv[4]

    departData = utility.openFile(departmentsFileName, '\t')

    scrapeCoursesFromWebreg(departData, outputFileName, quarterCode, cookie)


def scrapeCoursesFromWebReg(departData, outputName, quarterCode, cookie):
    courseData = getCourseCodesAndNames(departData, quarterCode, cookie)
    printCourseData(courseData, outputName)

def getCourseCodesAndNames(departData, quarterCode, cookie):

        courseData = []
        for i in range(0, len(departData)):

            departName = departData[i][0]
            url = utility.WEBREG_COURSES.format(departName,departName, quarterCode)
            #print(url)
            headers = {
            "Cookie": cookie
            }
            result = requests.get(url, headers=headers)
            #print(result.content)
            data = json.loads(result.content)
            for obj in data:
                courseData.append([obj["SUBJ_CODE"], obj["CRSE_CODE"]])

        return courseData

def printCourseData(courseData, filename):
    outputFile = open(filename, 'w')

    for course in courseData:
        outputFile.write(course[0] + "\t" + course[1] + '\n')


if __name__ == "__main__":
    main()
