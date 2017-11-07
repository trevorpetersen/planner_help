import sys
import requests
import json
import csv

from bs4 import BeautifulSoup


def main():
    filename = sys.argv[1]
    classes = getClassesFromFile(filename)

    for x in range(0, len(classes)):
        className = classes[x]
        #className = 'BIEB 121'
        url = "https://act.ucsd.edu/scheduleOfClasses/scheduleOfClassesStudentResult.htm"
        headers = {
        'Host': 'act.ucsd.edu',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'Origin': 'https://act.ucsd.edu',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent':
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer': 'https://act.ucsd.edu/scheduleOfClasses/scheduleOfClassesStudent.htm',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.8'
        }


        data = {
        "selectedTerm":"FA17",
        "xsoc_term": None,
        "loggedIn":"false",
        "tabNum": "tabs-crs",
        "_selectedSubjects":"1",
        "schedOption1":"true",
        "_schedOption1":"on",
        "_schedOption11":"on",
        "_schedOption12":"on",
        "schedOption2":"true",
        "_schedOption2":"on",
        "_schedOption4":"on",
        "_schedOption5":"on",
        "_schedOption3":"on",
        "_schedOption7":"on",
        "_schedOption8":"on",
        "_schedOption13":"on",
        "_schedOption10":"on",
        "_schedOption9":"on",
        "schDay":"M",
        "_schDay":"on",
        "schDay":"T",
        "_schDay":"on",
        "schDay":"W",
        "_schDay":"on",
        "schDay":"R",
        "_schDay":"on",
        "schDay":"F",
        "_schDay":"on",
        "schDay":"S",
        "_schDay":"on",
        "schStartTime":"12:00",
        "schStartAmPm":"0",
        "schEndTime":"12:00",
        "schEndAmPm":"0",
        "_selectedDepartments":"1",
        "schedOption1Dept":"true",
        "_schedOption1Dept":"on",
        "_schedOption11Dept":"on",
        "_schedOption12Dept":"on",
        "schedOption2Dept":"true",
        "_schedOption2Dept":"on",
        "_schedOption4Dept":"on",
        "_schedOption5Dept":"on",
        "_schedOption3Dept":"on",
        "_schedOption7Dept":"on",
        "_schedOption8Dept":"on",
        "_schedOption13Dept":"on",
        "_schedOption10Dept":"on",
        "_schedOption9Dept":"on",
        "schDayDept":"M",
        "_schDayDept":"on",
        "schDayDept":"T",
        "_schDayDept":"on",
        "schDayDept":"W",
        "_schDayDept":"on",
        "schDayDept":"R",
        "_schDayDept":"on",
        "schDayDept":"F",
        "_schDayDept":"on",
        "schDayDept":"S",
        "_schDayDept":"on",
        "schStartTimeDept":"12:00",
        "schStartAmPmDept":"0",
        "schEndTimeDept":"12:00",
        "schEndAmPmDept":"0",
        "courses": className,
        "sections": None,
        "instructorType":"begin",
        "instructor": None,
        "titleType":"contain",
        "title": None,
        "_hideFullSec":"on",
        "_showPopup":"on"
        }



        result = requests.post(url, headers=headers, data = data)
        soup = BeautifulSoup(result.content, "lxml")
        course_data = []

        if(len(soup.findAll("table")) < 2):
            continue

        table = soup.findAll("table")[1]
        table_rows = table.findAll("tr")

        columns = table_rows[2].findAll("td")
        for x in range(0, len(columns)):
            columns[x] = columns[x].text.strip()

        table_rows = table.findAll("tr", {'class': 'sectxt'})
        mostRecentTeacher = ''

        for x in range(0,len(table_rows)):
            weird = [];
            row_data = table_rows[x].findAll("td")
            if(len(row_data) < 12):
                continue
            if("DI" not in row_data[3].text.strip() and "LA" not in row_data[3].text.strip()):
                course = {}
                course['type'] = row_data[3].text.strip();
                course['discussions'] = []
                course['days'] = row_data[5].text.strip()
                course['time'] = row_data[6].text.strip()
                course['professor'] = row_data[9].text.strip()
                if '\n' in course['professor']:
                    course['professor'] = course['professor'][0:course['professor'].index('\n')]
                course['waitlist'] = row_data[10].text.strip()
                course['waitlist'] = course['waitlist'].replace("\t", "")
                course['waitlist'] = course['waitlist'].replace("\n", "")
                course['waitlist'] = course['waitlist'].replace("\r", "")
                course['limit'] = row_data[11].text.strip()
                course_data.append(course)
            else:
                if(len(course_data) == 0):
                    course = {}
                    course['type'] = row_data[3].text.strip();
                    course['discussions'] = []
                    course['days'] = row_data[5].text.strip()
                    course['time'] = row_data[6].text.strip()
                    course['professor'] = row_data[9].text.strip()
                    if '\n' in course['professor']:
                        course['professor'] = course['professor'][0:course['professor'].index('\n')]
                    course['waitlist'] = row_data[10].text.strip()
                    course['waitlist'] = course['waitlist'].replace("\t", "")
                    course['waitlist'] = course['waitlist'].replace("\n", "")
                    course['waitlist'] = course['waitlist'].replace("\r", "")
                    course['limit'] = row_data[11].text.strip()
                    weird.append(course)
                else:
                    course = course_data[len(course_data) - 1]
                    discussion = {}
                    discussion['days'] = row_data[5].text.strip()
                    discussion['time'] = row_data[6].text.strip()
                    discussion['waitlist'] = row_data[10].text.strip()
                    discussion['waitlist'] = discussion['waitlist'].replace("\t", "")
                    discussion['waitlist'] = discussion['waitlist'].replace("\n", "")
                    discussion['waitlist'] = discussion['waitlist'].replace("\r", "")
                    discussion['limit'] = row_data[11].text.strip()
                    course['discussions'].append(discussion)

        if len(course_data) > 0:
            for course in course_data:
                if(len(course['discussions']) > 0):
                    for discussion in course['discussions']:
                        sys.stdout.write(className + "\t" + course['type'] + "\t" + course['days'] + "\t" + course['time'] + "\t" + course['professor'] + "\t" + discussion['days'] + "\t" + discussion['time'] + "\t" + discussion['limit'] + "\t" + discussion['waitlist']  + "\n")
                        sys.stdout.flush()
                else:
                    #sys.stdout.write(className + "\t" + course['type'] + "\t" + course['days'] + "\t" + course['time'] + "\t" + course['professor'] + "\n")
                    sys.stdout.write(className + "\t" + course['type'] + "\t" + course['days'] + "\t" + course['time'] + "\t" + course['professor']  + "\tNULL\tNULL\t" +  course['limit'] + "\t" + course['waitlist']  + "\n")
                    sys.stdout.flush()

        for course in weird:
            sys.stdout.write(className + "\t" + course['type'] + "\t" + course['days'] + "\t" + course['time'] + "\t" + course['professor']  + "\tNULL\tNULL\t" +  course['limit'] + "\t" + course['waitlist']  + "\n")
            sys.stdout.flush()

        #sys.exit()
def getClassesFromFile(filename):
    classes = []
    with open(filename, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter= '\t')
        for row in reader:
            classes.append(row[0])

    return classes

main()
