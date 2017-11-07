import MySQLdb
import sys
import csv


def main():
    filename = sys.argv[1]
    array = getCoursesFromFile(filename)
    db = MySQLdb.connect(host="localhost",user="root",passwd="password", db="planner")
    cur = db.cursor()
    for c in array:
        insert = "INSERT INTO course_catalog (course_name) VALUES ( \'" + c + "\' )"

        print(insert)
        cur.execute(insert)
        db.commit()


def getCoursesFromFile(filename):
    array = []
    with open(filename, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter= '\t')
        for row in reader:
            array.append(row[0])

    return array

main()
