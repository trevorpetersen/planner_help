import utility
import getAvailableQuarters
import cred

import sys
import requests
import json
import getpass
import csv
from bs4 import BeautifulSoup

def main():
    print(getCookieWithPrompt())

def getCookieWithPrompt():
    username = raw_input("Username: ")
    password = getpass.getpass("Password: ")
    session = requests.Session()
    navigateToLogin(session)
    return login(session, username, password)

def getCookie(username, password):
    session = requests.Session()
    navigateToLogin(session)
    return login(session, username, password)

def navigateToLogin(session):
    result = session.get(utility.WEBREG_START)

def login(session, username, password):
    payload = {
    "initAuthMethod": "urn:mace:ucsd.edu:sso:studentsso",
    "submit": "submit",
    "urn:mace:ucsd.edu:sso:authmethod":"urn:mace:ucsd.edu:sso:studentsso",
    "urn:mace:ucsd.edu:sso:username": username,
    "urn:mace:ucsd.edu:sso:password": password
    }

    #print(session.cookies.get_dict())
    result = session.post(utility.WEBREG_LOGIN, data = payload)

    soup = BeautifulSoup(result.content, "lxml")
    redirectForm = soup.find("form")
    nextURL = redirectForm["action"]

    inputs = redirectForm.findAll("input");

    payload = {}
    for formInput in inputs:
        name = formInput.get("name")
        value = formInput.get("value")
        if name != None:
            payload[name] = value

    #print(payload)
    payload["submit"] = "submit"
    result = session.post(nextURL, data = payload)

    terms = getAvailableQuarters.getAvailableQuartersUsingSession(session)
    for term in terms:
        loadWebregStuff(session, term["termCode"], term["seqId"])

    cookies = session.cookies.get_dict()

    cookieString = ""
    for key in cookies:
        cookieString = cookieString + key + "=" + cookies[key] + "; "
    #print(cookieString)
    return cookieString



def loadWebregStuff(session, quarterCode, seqID):
    result = session.get("https://act.ucsd.edu/webreg2/svc/wradapter/get-status-start?termcode={0}&seqid={1}".format(quarterCode, seqID))
    #print(result.content)
    result = session.get("https://act.ucsd.edu/webreg2/svc/wradapter/check-eligibility?termcode={0}&seqid={1}&logged=true".format(quarterCode, seqID))
    #print(result.content)
    result = session.get("https://act.ucsd.edu/webreg2/svc/wradapter/get-msg-to-proceed?termcode={0}".format(quarterCode))
    #print(result.content)
    result = session.get("https://act.ucsd.edu/webreg2/main?p1={0}&p2=UN".format(quarterCode))
    #print(result.content)

if __name__ == "__main__":
    main()
