import utility
import sys
import requests
import json

from bs4 import BeautifulSoup

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

def main():

    utility.checkInput(["outputFile"],[])
    outputFilename = sys.argv[1]
    scrapeDepartments(outputFilename)


def scrapeDepartments(filename):
    departData = getDepartCodesAndNames()
    utility.printData(departData, filename)

def getDepartCodesAndNames():

    departData = []
    for i in range (0, len(letters)):
        utility.updateStatus("Getting departments that start with " + letters[i].upper())
        url = utility.DEPARTMENT_URL + letters[i].upper()
        result = requests.get(url)
        soup = BeautifulSoup(result.content, "lxml")
        table = soup.table
        if(table == None):
            continue
        classes = table.findAll('li')

        for x in range(0, len(classes)):
            depart = classes[x]
            departStuff = depart.text.split('-')
            departCode = departStuff[0].strip()
            departName = departStuff[1].strip()
            departData.append({"DepartCode": departCode, "DepartName":departName})

    sys.stdout.write('\n')
    return departData

if __name__ == "__main__":
    main()
