import utility
import scrapeDepartments
import scrapeCoursesFromWebReg
import cookieHelper
import getAvailableQuarters

import sys
import requests
import json
from bs4 import BeautifulSoup


def main():

    utility.checkInput(["outputFile", "quarterCode"], [])
    utility.checkCred()

    outputFilename = sys.argv[1]
    quarterCode = sys.argv[2]
    cookie = utility.getCookie()

    print("Scraping departments...")
    departData = scrapeDepartments.getDepartCodesAndNames()
    print("Scraping courses ...")
    courseData = scrapeCoursesFromWebReg.getCourseCodesAndNames(departData, quarterCode, cookie)
    scrapeCoursesFromWebReg.printCourseData(courseData, outputFilename)



if __name__ == "__main__":
    main()
