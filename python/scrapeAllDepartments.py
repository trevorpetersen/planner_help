import sys
import requests
import json

from bs4 import BeautifulSoup

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

for i in range (0, len(letters)):
    url = 'http://courses.ucsd.edu/?u_letter=' + letters[i].upper()
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
        print(courseCode + "\t" + courseName)
