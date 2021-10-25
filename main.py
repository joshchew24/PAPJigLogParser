import sys
import re
import parser as p

if len(sys.argv) != 2:
     exit("Usage: \'python parser.py arg1\'\narg1 is the path/filename of .log file to be parsed.")

file = sys.argv[1]

pattern = re.compile("app_20(1|2)\\d(0|1)\\d[0-3]\\d\\.log")
m = pattern.search(file)

if not m:
    exit("Error: filename should be of format \'app_YYYYMMDD.log\'")

filename = m.group()

if (len(filename) != 16): 
    exit("Error: filename should be of format \'app_YYYYMMDD.log\'")

f = open(file, "r")
lines = f.readlines()
f.close()

date = filename[4:12]

trimmed = open("outputs/" + date + "-TRIMMED.log", "w")
tempLog = open("outputs/" + date + "-temps.log", "w")
tempCSV = open("outputs/" + date + "-temps.csv", "w")

for line in lines:
    if p.isNotFluff(line):
        trimmed.write(line)
    if p.containsTempDataPoint(line):
        tempLog.write(p.formatToTemps(line))
        tempCSV.write(p.formatToCSV(line))

trimmed.close()
tempLog.close()
tempCSV.close()