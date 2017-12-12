import sys
import csv
import requests

DEPARTMENT_URL = 'http://courses.ucsd.edu/?u_letter='
CLASSES_URL = 'http://www.ucsd.edu/catalog/courses/'
WEBREG_COURSES = "https://act.ucsd.edu/webreg2/svc/wradapter/secure/search-by-all?subjcode=&crsecode={0}&department=&professor=&title=&levels=&days=&timestr=&opensection=false&isbasic=true&basicsearchvalue={1}&termcode={2}"
WEBREG_START = "https://act.ucsd.edu/webreg2/start"
WEBREG_LOGIN = "https://a4.ucsd.edu/tritON/Authn/UserPassword"
WEBREG_AVAILABLE_QUARTERS = "https://act.ucsd.edu/webreg2/svc/wradapter/get-term"

def checkInput(numFiles, req, opt):
    if len(sys.argv) != numFiles + 1:
        printUsage(req, opt)
        sys.exit(1)

def printUsage(required, optional=[]):
    outputText = ''

    for req in required:
        outputText += ' ' + req

    for opt in optional:
        outputText += ' [' + opt + ']'

    print("Usage: " + sys.argv[0] + outputText)


def openFile(filename, delin):
    output = []
    with open(filename, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter= delin)
        for row in reader:
            output.append(row)

    return output
