import sys
import re

def isNotFluff(line):
    # return false if contains any of these 4 keywords, 
    removeIfContains = ["Sending", "Writing", "Received", "Raising"]
    for key in removeIfContains:
        keyAsRegex = re.compile(key)
        found = keyAsRegex.search(line)
        if not found:
            continue
        else: 
            return False
    # return false if line is too short
    return len(line) > 8

def containsTempDataPoint(line):
    pattern = re.compile("controller: \\d{1,3}\\.\\d{3}  corrected: \\d{1,3}\\.\\d{3}")
    found = pattern.search(line)
    if not found:
        return False
    else: 
        return True

def formatToTemps(line):
    timePattern = re.compile("\\d\\d:\\d\\d:\\d\\d,\\d{3}")
    timeMatch = timePattern.search(line)
    timeWithComma = timeMatch.group()
    time = timeWithComma.replace(",", ".")

    tempPattern = re.compile(" controller: \\d{1,3}\\.\\d{3}  corrected: \\d{1,3}\\.\\d{3}")
    tempMatch = tempPattern.search(line)
    temp = tempMatch.group()

    return time + " " + temp + "\n"


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

trimmed = open(date + "-TRIMMED.log", "w")
tempLog = open(date + "-temps.log", "w")

for line in lines:
    if isNotFluff(line):
        trimmed.write(line)
    if containsTempDataPoint(line):
        tempLog.write(formatToTemps(line))
        #tempCsv.write(formatToCSV(line))

trimmed.close()
tempLog.close()

