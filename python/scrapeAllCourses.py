import utility
import time
import sys
import requests
import json
from bs4 import BeautifulSoup

def main():
    utility.checkInput(2, ['departments', 'outputFile']);

    filename = sys.argv[1]
    outputFileName = sys.argv[2]

    departments = utility.openFile(filename,'\t')

    outputFile = open(outputFileName, 'w')
    seen = {}

    for i in range(0, len(departments)):
        departCode = departments[i][0]
        url = utility.CLASSES_URL + departCode + '.html'
        time.sleep(0.1)
        result = requests.get(url)
        soup = BeautifulSoup(result.content, "lxml")

        courses = soup.findAll("p", { "class" : "course-name" })

        for course in courses :
            name = course.text.split('.')[0].encode('utf-8').strip()
            name = clean(name)
            outputFile.write(name +  '\n')
        continue
        sys.exit()

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

def clean(text):
    while "  " in text:
        text = text.replace("  ", " ")
    while "\t\t" in text:
        text = text.replace("\t\t", "\t")
    while "\n" in text:
        text = text.replace("\n", "")

    text = text.replace("\t ", "\t")
    if '/' in text:
        text = text.split('/')[0]

    return text

if __name__ == "__main__":
    main()
