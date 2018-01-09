import utility
import departments
import courses
import courseData
import cookieHelper

import sys
import requests
import json
from bs4 import BeautifulSoup


def main():

    utility.checkInput(["departOutputFile", "courseListOutputFile", "courseDataOutputFile", "quarterCode"], [])
    utility.checkCred()

    outputDepart = sys.argv[1]
    outputCourseList = sys.argv[2]
    outputCourseData = sys.argv[3]

    quarterCode = sys.argv[4]

    cookie = utility.getCookie()

    print("Scraping departments...")
    departData = departments.getDepartCodesAndNames()
    utility.printData(departData, outputDepart)
    print("Scraping courses ...")
    coursesData = courses.getCourseCodesAndNames(departData, quarterCode, cookie)
    utility.printData(coursesData, outputCourseList)
    print("Scraping data for all courses ...")
    extraCourseData = courseData.getCourseData(coursesData, quarterCode, cookie)
    utility.printData(extraCourseData, outputCourseData)



if __name__ == "__main__":
    main()
