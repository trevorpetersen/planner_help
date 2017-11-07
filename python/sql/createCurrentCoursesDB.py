import csv
import sys

def main():
    getClassesFromFile(sys.argv[1])



def getClassesFromFile(filename):
    with open(filename, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter= '\t')
        for row in reader:
            for x in range(0,len(row)):
                sys.stdout.write(row[x] + ' TEXT,')
            return

main()
