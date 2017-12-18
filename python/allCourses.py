import utility
import time
import sys
import requests
import json
from bs4 import BeautifulSoup

def main():
    utility.checkInput(['departmentsFile', 'outputFile']);

    filename = sys.argv[1]
    outputFileName = sys.argv[2]

    departments = utility.processData(filename,'\t')

    allCourses = getCourseCodesAndNames(departments)
    utility.printData(allCourses, outputFileName)

def getCourseCodesAndNames(departData):
    allCourses = []
    for i in range(0, len(departData)):
        departCode = departData[i]['DepartCode']
        utility.updateStatus("Getting courses for " + departCode)
        url = utility.CLASSES_URL + departCode + '.html'
        time.sleep(0.1)
        result = requests.get(url)
        soup = BeautifulSoup(result.content, "lxml")

        courses = soup.findAll("p", { "class" : "course-name" })

        for course in courses :

            fullName = course.text.split('.')[0].encode('utf-8').strip()
            fullName = clean(fullName)

            if(len(fullName.split(' ')) == 2):
                subject = fullName.split(' ')[0]
                classCode = fullName.split(' ')[1]

                allCourses.append({"SUBJ_CODE": subject, "CRSE_CODE": classCode})

    sys.stdout.write('\n')
    return allCourses

def clean(text):
    while "\t" in text:
        text = text.replace("\t\t", " ")
    while "  " in text:
        text = text.replace("  ", " ")
    while "\n" in text:
        text = text.replace("\n", "")

    text = text.replace("\t ", "\t")
    if '/' in text:
        text = text.split('/')[0]

    return text

if __name__ == "__main__":
    main()
