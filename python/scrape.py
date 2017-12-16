import utility
import scrapeDepartments
import scrapeCoursesFromWebReg
import scrapeWebReg
import cookieHelper
import getAvailableQuarters

import sys
import requests
import json
from bs4 import BeautifulSoup


def main():

    utility.checkInput(["quarterCode", "departOutputFile", "courseListOutputFile", "courseDataOutputFile"], [])
    utility.checkCred()

    quarterCode = sys.argv[1]

    outputDepart = sys.argv[2]
    outputCourseList = sys.argv[3]
    outputCourseData = sys.argv[4]

    cookie = utility.getCookie()

    print("Scraping departments...")
    departData = scrapeDepartments.getDepartCodesAndNames()
    utility.printData(departData, outputDepart)
    print("Scraping courses ...")
    courseData = scrapeCoursesFromWebReg.getCourseCodesAndNames(departData, quarterCode, cookie)
    utility.printData(courseData, outputCourseList)
    print("Scraping data for all courses ...")
    extraCourseData = scrapeWebReg.getCourseData(courseData, cookie)
    utility.printData(extraCourseData, outputCourseData)



if __name__ == "__main__":
    main()
