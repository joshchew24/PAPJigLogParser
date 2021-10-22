import sys
import re

# print ('Number of arguments:', len(sys.argv), 'arguments.')
# print ('Argument List:', str(sys.argv))

if len(sys.argv) != 2:
     exit("Usage: \'python parser.py arg1\'\narg1 is the name of .log file to be parsed.")

filename = sys.argv[1]
if (len(filename) != 16): 
    exit("Error: filename should be of format \'app_YYYYMMDD.log\'")

pattern = re.compile("app_20(1|2)\\d(0|1)\\d[0-3]\\d\\.log")
m = pattern.match(filename)
if not m:
    exit("Error: filename should be of format \'app_YYYYMMDD.log\'")


print(m)
print(filename)

