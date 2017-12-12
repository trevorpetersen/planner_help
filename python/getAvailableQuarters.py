import utility
import getCookie
import sys
import csv
import requests
import json


def main():

    argCount = len(sys.argv)
    if(argCount == 1):
        cook = getCookie.getCookie();
        print("Getting cookies ...")
    elif (argCount == 2):
        cook = sys.argv[1]
    else:
        utility.printUsage([], ["cookie"])
        sys.exit(1)


    data = getAvailableQuarters(cook)
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
