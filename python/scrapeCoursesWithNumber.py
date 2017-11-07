import sys
import requests
import json
import csv

from bs4 import BeautifulSoup


def main():
    filename = sys.argv[1]
    classes = getClassesFromFile(filename)
    scrapeSecondSource(classes)

def scrapeFirstSource(classes):
    for x in range(0, len(classes)):
        url = "http://ucsd.edu/catalog/courses/" + classes[x] + ".html"

        result = requests.get(url)
        soup = BeautifulSoup(result.content, "lxml")

        allClasses = soup.findAll("p", {"class": "course-name"});

        for course in allClasses:
            if("." in course.text):
                strings = course.text.split(".");
                courseName = strings[0].encode('utf-8').strip();
                courseName.replace("\n", "");
                courseName.replace("\t", "");

                print(courseName)

def scrapeSecondSource(classes):
    for x in range(0, len(classes)):
        url = "http://courses.ucsd.edu/courseList.aspx?name=" + classes[x]

        result = requests.get(url)
        soup = BeautifulSoup(result.content, "lxml")

	table = soup.find('table')

	if(table == None):
		continue

	allCourses = table.findAll('li');
	for course in allCourses:
		print(course.text.split('-')[0].encode('utf-8').strip())



def getClassesFromFile(filename):
    classes = []
    with open(filename, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter= '\t')
        for row in reader:
            classes.append(row[0])

    return classes

main()
