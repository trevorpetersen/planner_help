import utility
import sys
import requests
import json

from bs4 import BeautifulSoup

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

def main():

    utility.checkInput(1,["[outputFile]"])
    outputFilename = sys.argv[1]
    scrapeDepartments(outputFilename)


def scrapeDepartments(filename):
    courseData = getDepartCodesAndNames()
    printDepartData(courseData, filename)

def getDepartCodesAndNames():

    courseData = []
    for i in range (0, len(letters)):
        url = utility.DEPARTMENT_URL + letters[i].upper()
        result = requests.get(url)
        soup = BeautifulSoup(result.content, "lxml")
        table = soup.table
        if(table == None):
            continue
        classes = table.findAll('li')

        for x in range(0, len(classes)):
            course = classes[x]
            courseStuff = course.text.split('-')
            courseCode = courseStuff[0].strip()
            courseName = courseStuff[1].strip()
            courseData.append([courseCode, courseName])

    return courseData

def printDepartData(departData, filename):
    outputFile = open(filename, 'w')

    for depart in departData:
        outputFile.write(depart[0] + "\t" + depart[1] + '\n')



if __name__ == "__main__":
    main()
