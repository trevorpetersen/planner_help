import sys
import requests
import json
import csv

from bs4 import BeautifulSoup

def main():
    isFirst = True
    filename = sys.argv[1]
    classes = getClassesFromFile(filename)

    for x in range(0, len(classes)):

        className = classes[x]
        while('  ' in className):
            className = className.replace('  ', ' ')
        split = className.split(' ')
        url = "https://act.ucsd.edu/webreg2/svc/wradapter/secure/search-load-group-data?subjcode={0}&crsecode={1}&termcode=WI18&_=1510110426749"
        headers = {
        "Cookie": ""
        }
        prefix = ''
        for y in range(0,6):
            formatted = url.format(split[0].strip() ,prefix + split[1].strip());
            result = requests.get(formatted, headers=headers)
            if result.status_code != 200:
                break
            data = json.loads(result.content)
            if(len(data) > 0):
                break
            prefix += '+'

        if(len(data) == 0):
            continue

        if(isFirst and len(data) > 0):
            isFirst = False
            printHeaders()

        for obj in data:
            printData(obj, className)




def getClassesFromFile(filename):
    classes = []
    with open(filename, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter= '\t')
        for row in reader:
            classes.append(row[0])

    return classes

def printData(obj, className):
    sys.stdout.write(className + '\t')
    sys.stdout.flush()
    printVal(obj,'PERSON_FULL_NAME')
    printVal(obj,'BEGIN_HH_TIME')
    printVal(obj,'SECTION_END_DATE')
    printVal(obj,'AVAIL_SEAT')
    printVal(obj,'DAY_CODE')
    printVal(obj,'BLDG_CODE')
    printVal(obj,'BEGIN_MM_TIME')
    printVal(obj,'FK_CDI_INSTR_TYPE')
    printVal(obj,'FK_SPM_SPCL_MTG_CD')
    printVal(obj,'COUNT_ON_WAITLIST')
    printVal(obj,'END_HH_TIME')
    printVal(obj,'PRIMARY_INSTR_FLAG')
    printVal(obj,'LONG_DESC')
    printVal(obj,'END_MM_TIME')
    printVal(obj,'SECTION_START_DATE')
    printVal(obj,'STP_ENRLT_FLAG')
    printVal(obj,'SCTN_ENRLT_QTY')
    printVal(obj,'START_DATE')
    printVal(obj,'ROOM_CODE')
    printVal(obj,'SECTION_NUMBER')
    printVal(obj,'SECT_CODE')
    printVal(obj,'BEFORE_DESC')
    printVal(obj,'SCTN_CPCTY_QTY')
    printVal(obj,'FK_SST_SCTN_STATCD')
    sys.stdout.write('\n')
    sys.stdout.flush()


def printHeaders():
    sys.stdout.write('CLASS_NAME')
    sys.stdout.write('\t')
    sys.stdout.write('PERSON_FULL_NAME')
    sys.stdout.write('\t')
    sys.stdout.write('BEGIN_HH_TIME')
    sys.stdout.write('\t')
    sys.stdout.write('SECTION_END_DATE')
    sys.stdout.write('\t')
    sys.stdout.write('AVAIL_SEAT')
    sys.stdout.write('\t')
    sys.stdout.write('DAY_CODE')
    sys.stdout.write('\t')
    sys.stdout.write('BLDG_CODE')
    sys.stdout.write('\t')
    sys.stdout.write('BEGIN_MM_TIME')
    sys.stdout.write('\t')
    sys.stdout.write('FK_CDI_INSTR_TYPE')
    sys.stdout.write('\t')
    sys.stdout.write('FK_SPM_SPCL_MTG_CD')
    sys.stdout.write('\t')
    sys.stdout.write('COUNT_ON_WAITLIST')
    sys.stdout.write('\t')
    sys.stdout.write('END_HH_TIME')
    sys.stdout.write('\t')
    sys.stdout.write('PRIMARY_INSTR_FLAG')
    sys.stdout.write('\t')
    sys.stdout.write('LONG_DESC')
    sys.stdout.write('\t')
    sys.stdout.write('END_MM_TIME')
    sys.stdout.write('\t')
    sys.stdout.write('SECTION_START_DATE')
    sys.stdout.write('\t')
    sys.stdout.write('STP_ENRLT_FLAG')
    sys.stdout.write('\t')
    sys.stdout.write('SCTN_ENRLT_QTY')
    sys.stdout.write('\t')
    sys.stdout.write('START_DATE')
    sys.stdout.write('\t')
    sys.stdout.write('ROOM_CODE')
    sys.stdout.write('\t')
    sys.stdout.write('SECTION_NUMBER')
    sys.stdout.write('\t')
    sys.stdout.write('SECT_CODE')
    sys.stdout.write('\t')
    sys.stdout.write('BEFORE_DESC')
    sys.stdout.write('\t')
    sys.stdout.write('SCTN_CPCTY_QTY')
    sys.stdout.write('\t')
    sys.stdout.write('FK_SST_SCTN_STATCD')
    sys.stdout.write('\n')
    sys.stdout.flush()


def printVal(obj, val):
    if val == 'PERSON_FULL_NAME' and val in obj:
        name = str(obj[val]);
        name = name.split(';')[0].strip()
        sys.stdout.write(name + '\t')
        sys.stdout.flush()
        return
    if val in obj:
        sys.stdout.write(str(obj[val]) + '\t')
        sys.stdout.flush()
    else:
        sys.stdout.write("" + '\t')
        sys.stdout.flush()


main()
