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
        url = "http://www.cape.ucsd.edu/responses/Results.aspx?Name=&CourseNumber={0}";
        url = url.format(className);
        headers = {
        "Connection": "keep-alive",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.8"
        }

        result = requests.get(url, headers=headers)
        soup = BeautifulSoup(result.content, "lxml")
        course_data = []


        table = soup.table
        columns = table.tr.findAll("th")
        columns_length = len(columns)

        for x in range(0, columns_length):
            columns[x] = columns[x].text.strip()

        table_body = table.tbody

        if(table_body == None):
            continue


        table_rows = table_body.findAll("tr")
        table_rows_length = len(table_rows)

        for x in range(0, table_rows_length):
            course = {}
            row_data = table_rows[x].findAll('td')
            for y in range(0, columns_length):
                course[columns[y]] = row_data[y].text.strip()
            course_data.append(course)
            for value in course.values():
                #print(value + "\t")
                sys.stdout.write(value + "\t")
            sys.stdout.write("\n")
            sys.stdout.flush()




def getClassesFromFile(filename):
    classes = []
    with open(filename, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter= '\t')
        for row in reader:
            classes.append(row[0])

    return classes


main();
