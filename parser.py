import sys
import re

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
print(lines)


# with open(file, "r") as f:
#     lines = f.readlines()

# date = filename[4:12]

# with open(file, "w") as f:
#     for line in lines:
#         if line.strip("\n") != "bonk":
#             f.write(line)

