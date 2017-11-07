import MySQLdb
import sys
import csv


def main():
    na = "N/A"
    filename = sys.argv[1]
    capes = getCapesFromFile(filename)
    db = MySQLdb.connect(host="localhost",user="root",passwd="password", db="planner")
    cur = db.cursor()
    for c in capes:
        insert = "INSERT INTO cape_data"
        columns = " (instructor, course, term, enroll, evals_made, rcmnd_class, rcmnd_instr, study_hours, avg_grade_expected, avg_grade_received)"
        values = " VALUES ({0},{1},{2},{3},{4},{5},{6},{7},{8},{9})"

        inst = c[8]
        if(inst == na):
            inst = 'NULL'
        else:

            inst = '\"' + inst + '\"'
        cou = c[4]
        if(cou == na):
            cou = 'NULL'
        else:
            cou = '\"' + cou + '\"'


        ter = c[0]
        if(ter == na):
            ter = 'NULL'
        else:
            ter = '\"' + ter + '\"'

        enr = c[2]
        if(enr == na):
            enr = 'NULL'

        eva = c[7]
        if(eva == na):
            eva = 'NULL'

        rcc = c[1]
        if(rcc == na):
            rcc = 'NULL'
        else:
            rcc = c[1][:-1]

        rci = c[5]
        if(rci == na):
            rci = 'NULL'
        else:
            rci =c[5][:-1]

        sth = c[3]
        if(sth == na):
            sth = 'NULL'

        avgg = c[6]
        if(avgg == na):
            avgg = 'NULL'
        else:
            avgg = '\"' + avgg + '\"'

        avgr = c[9]
        if(avgr == na):
            avgr = 'NULL'
        else:
            avgr = '\"' + avgr + '\"'


        values = values.format(inst, cou, ter, enr, eva, rcc,rci, sth,avgg,avgr)
        print(insert + columns + values)
        cur.execute(insert + columns + values)
        db.commit()


def getCapesFromFile(filename):
    capes = []
    with open(filename, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter= '\t')
        for row in reader:
            capes.append(row)

    return capes

main()
