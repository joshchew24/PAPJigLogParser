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
# print ('Number of arguments:', len(sys.argv), 'arguments.')
# print ('Argument List:', str(sys.argv))

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

o = open(date + "-test.log", "w")
for line in lines:
    if isNotFluff(line):
        o.write(line)

o.close()


# with open(file, "r") as f:
#     lines = f.readlines()


# with open(file, "w") as f:
#     for line in lines:
#         if line.strip("\n") != "bonk":
#             f.write(line)

