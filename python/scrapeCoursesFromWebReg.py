import utility
import cred

import sys
import requests
import json
import csv
from bs4 import BeautifulSoup

def main():
    utility.checkInput(["departmentsFile", "outputFile", "QuarterCode"],[])
    utility.checkCred()

    departmentsFileName = sys.argv[1]
    outputFileName = sys.argv[2]
    quarterCode = sys.argv[3]
    cookie = utility.getCookie()

    departData = utility.processData(departmentsFileName, '\t')

    scrapeCoursesFromWebReg(departData, outputFileName, quarterCode, cookie)


def scrapeCoursesFromWebReg(departData, outputName, quarterCode, cookie):
    courseData = getCourseCodesAndNames(departData, quarterCode, cookie)
    utility.printData(courseData, outputName)

def getCourseCodesAndNames(departData, quarterCode, cookie):

        courseData = []
        for i in range(0, len(departData)):

            departName = departData[i]["DepartCode"]
            utility.updateStatus("Getting courses for " + departName)
            url = utility.WEBREG_COURSES.format(departName,departName, quarterCode)
            headers = {
            "Cookie": cookie
            }
            result = requests.get(url, headers=headers)
            data = json.loads(result.content)
            for obj in data:
                courseData.append(obj)

        sys.stdout.write('\n')
        return courseData

def printCourseData(courseData, filename):
    outputFile = open(filename, 'w')

    if(len(courseData) > 0):
        keys = list(courseData[0].keys())

        headers = ""
        for i in range(0, len(keys)):
            if(i == 0):
                headers += keys[i]
            else:
                headers += "\t" + keys[i]

        outputFile.write(headers + '\n')


    for course in courseData:
        row = ''
        for i in range(0, len(keys)):
            if(i == 0):
                row += str(course[keys[i]])
            else:
                row += "\t" + str(course[keys[i]])

        outputFile.write(row + '\n')
    outputFile.close()

if __name__ == "__main__":
    main()
