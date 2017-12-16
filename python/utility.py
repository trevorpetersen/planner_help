import cred
import cookieHelper

import sys
import csv
import requests

DEPARTMENT_URL = 'http://courses.ucsd.edu/?u_letter='
CLASSES_URL = 'http://www.ucsd.edu/catalog/courses/'
WEBREG_COURSES = "https://act.ucsd.edu/webreg2/svc/wradapter/secure/search-by-all?subjcode=&crsecode={0}&department=&professor=&title=&levels=&days=&timestr=&opensection=false&isbasic=true&basicsearchvalue={1}&termcode={2}"
WEBREG_START = "https://act.ucsd.edu/webreg2/start"
WEBREG_LOGIN = "https://a4.ucsd.edu/tritON/Authn/UserPassword"
WEBREG_AVAILABLE_QUARTERS = "https://act.ucsd.edu/webreg2/svc/wradapter/get-term"
WEBREG_COURSE_DATA = "https://act.ucsd.edu/webreg2/svc/wradapter/secure/search-load-group-data?subjcode={0}&crsecode={1}&termcode=WI18"

def checkInput(req, opt):
    if len(sys.argv) != len(req) + 1:
        printUsage(req, opt)
        sys.exit(1)

def checkCred():
    if(cred.cookie != ''):
        return
    if(cred.username != '' and cred.password != ''):
        return

    print('Error: Please add a username/password or cookie to cred.py and retry\n')
    sys.exit(1)

def getCookie():
    checkCred();
    if(cred.cookie != ''):
        return cred.cookie
    else:
        return cookieHelper.getCookie(cred.username, cred.password)

def printUsage(required, optional=[]):
    outputText = ''

    for req in required:
        outputText += ' ' + req

    for opt in optional:
        outputText += ' [' + opt + ']'

    print("Usage: python " + sys.argv[0] + outputText)

def printData(courseData, filename):
    outputFile = open(filename, 'w')

    if(len(courseData) > 0):
        keys = list(courseData[0].keys())

        headers = ""
        for i in range(0, len(keys)):
            if(i == 0):
                headers += keys[i]
            else:
                headers += "\t" + keys[i]

        outputFile.write(headers + '\n')


    for course in courseData:
        row = ''
        for i in range(0, len(keys)):
            if(i == 0):
                row += str(course[keys[i]])
            else:
                row += "\t" + str(course[keys[i]])

        outputFile.write(row + '\n')
    outputFile.close()


def openFile(filename, delin):
    output = []
    with open(filename, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter= delin)
        for row in reader:
            output.append(row)

    return output

def processRow(headers,row):
    """
    Stores the data from the row into a dictionary
    Key : Column Name
    """
    dataRow = {k : v for (k,v) in zip(headers,row) }
    return dataRow


def processData(filename, delin):
    """
    Main function to prcess the csv
    """
    data = []
    with open(filename,'r') as tsvfile:
        reader = csv.reader(tsvfile, delimiter=delin)
        headers = next(reader)
        for row in reader:
            dataRow = processRow(headers,row)
            data.append(dataRow)
    return data
