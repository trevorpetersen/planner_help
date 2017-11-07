import MySQLdb
import sys
import csv


def main():
    filename = sys.argv[1]
    capes = getCapesFromFile(filename)
    db = MySQLdb.connect(host="localhost",user="root",passwd="password", db="planner")
    cur = db.cursor()
    for c in capes:
        insert = "INSERT INTO current_classes"
        columns = getColumns(filename)
        values = " VALUES ({0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12},{13},{14},{15},{16},{17},{18},{19},{20},{21},{22},{23},{24})"

        for i in range(0, len(c)):
            c[i] = getVal(c[i], i);

        values = values.format(c[0],c[1],c[2],c[3],c[4],c[5],c[6],c[7],c[8],c[9],c[10],c[11],c[12],c[13],c[14],c[15],c[16],c[17],c[18],c[19],c[20],c[21],c[22],c[23],c[24])
        print(insert + columns + values)
        cur.execute(insert + columns + values)
        db.commit()

def getVal(val, index):
    ter = val
    if(ter == '' or ter == ' ' or ter == '  '):
        ter = 'NULL'
    elif(index == 2 or index == 4 or index == 5 or index == 7 or index == 10 or index == 11 or index == 14 or index == 17 or index == 20 or index == 23):
        ter = ter 
    else:
        ter = '\"' + ter + '\"'

    return ter

def getCapesFromFile(filename):
    capes = []
    with open(filename, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter= '\t')
        first = True
        for row in reader:
            if(first):
                first = False
                continue
            capes.append(row)

    return capes

def getColumns(filename):
    stuff = ' ('
    with open(filename, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter= '\t')
        for row in reader:
            for x in range(0,len(row)):
                if(x + 1 >= len(row)):
                    stuff += row[x] + " "
                else:
                    stuff += row[x] + ", "
            stuff += ') '
            return stuff

main()
