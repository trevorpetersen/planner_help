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

def getAvailableQuarters(cookie):
    url = utility.WEBREG_AVAILABLE_QUARTERS
    headers = {
    "Cookie": cookie
    }
    result = requests.get(url, headers= headers)
    return json.loads(result.content)

def getAvailableQuartersUsingSession(session):
    url = utility.WEBREG_AVAILABLE_QUARTERS
    result = session.get(url)
    return json.loads(result.content)

if __name__ == "__main__":
    main()
