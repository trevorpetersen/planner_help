import utility
import cred

import sys
import csv
import requests
import json


def main():

    utility.checkCred()
    cookie = utility.getCookie()

    data = getAvailableQuarters(cookie)
    for term in data:
        print(term["termDesc"] + "\n\t " + "Code: " + str(term["termCode"]))


def isValidQuarterCode(quarterCode, cookie):
    data = getAvailableQuarters(cookie)
    isValid = False
    for term in data:
        if( str(term["termCode"]) == quarterCode ):
            isValid = True
            break
    return isValid

def getAvailableQuarters(cookie):
    url = utility.WEBREG_AVAILABLE_QUARTERS
    headers = {
    "Cookie": cookie
    }
    result = requests.get(url, headers= headers)
    result = json.loads(result.content)

    validTerms = []
    for term in result:
        termCode = term["termCode"]
        result2 = requests.get(utility.WEBREG_CHECK_QUARTER.format(termCode, ""), headers= headers)
        result2 = json.loads(result2.content)
        if(result2["OPS"] == "SUCCESS"):
            validTerms.append(term)

    return validTerms

def getAvailableQuartersUsingSession(session):
    url = utility.WEBREG_AVAILABLE_QUARTERS
    result = session.get(url)
    return json.loads(result.content)

if __name__ == "__main__":
    main()
