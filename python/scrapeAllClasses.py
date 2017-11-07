import sys
import requests
import json
import csv
from bs4 import BeautifulSoup

def main():
    checkInput();

    filename = sys.argv[1]
    departments = getDepartmentsFromFile(filename)
    seen = {}

    for i in range(0, len(departments)):
        url = 'http://courses.ucsd.edu/courseList.aspx?name='
        url = url + departments[i]
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
            if(courseCode not in seen):
                print(courseCode + "\t" + courseName)
                seen[courseCode] = courseCode + "\t" + courseName



def checkInput():
    if len(sys.argv) != 2:
        print("Please provide a file")
        sys.exit(1)

def getDepartmentsFromFile(filename):
    departments = []
    with open(filename, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter= '\t')
        for row in reader:
            departments.append(row[0])

    return departments


main()
