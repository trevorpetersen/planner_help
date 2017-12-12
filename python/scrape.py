import utility
import scrapeDepartments
import scrapeCoursesFromWebReg
import getCookie
import getAvailableQuarters

import sys
import requests
import json
from bs4 import BeautifulSoup


def main():

    argCount = len(sys.argv)
    if(argCount == 3):
        cook = getCookie.getCookie()
        print("Getting cookies ...")

    elif (argCount == 4):
        cook = sys.argv[3]
    else:
        utility.printUsage(["outputFile", "quarterCode"], ["cookie"])
        sys.exit(1)

    outputFilename = sys.argv[1]
    quarterCode = sys.argv[2]

    print("Scraping departments...")
    departData = scrapeDepartments.getDepartCodesAndNames()
    print("Scraping courses ...")
    courseData = scrapeCoursesFromWebReg.getCourseCodesAndNames(departData, quarterCode, cook)
    scrapeCoursesFromWebReg.printCourseData(courseData, outputFilename)



if __name__ == "__main__":
    main()
