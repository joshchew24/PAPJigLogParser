import sys
import re
import log_parser as p
import grapher as g

if len(sys.argv) != 2:
     exit("Usage: \'main.py arg1\'\narg1 is the path/filename of .log file to be parsed.")

file = sys.argv[1]

pattern = re.compile("app_20(1|2)\\d(0|1)\\d[0-3]\\d\\.log")
m = pattern.search(file)

if not m:
    exit("Error: filename should be of format \'app_YYYYMMDD.log\'")

filename = m.group()

if (len(filename) != 16): 
    exit("Error: filename should be of format \'app_YYYYMMDD.log\'")

try:
    f = open(file, "r")
except FileNotFoundError as e:
    quit("Error: File not found. Verify it exists in the specified directory.")

lines = f.readlines()
f.close()

date = filename[4:12]

trimmed = open("outputs/" + date + "-TRIMMED.log", "w")
templog = open("outputs/" + date + "-temps.log", "w")
tempCSV = open("outputs/" + date + "-temps.csv", "w")

first_line_found = False

for line in lines:
    if p.is_not_fluff(line):
        trimmed.write(line)
    if p.contains_temp_data_points(line):
        if not first_line_found:
            first_line_found = True
            p.set_init_time(line)
        templog.write(p.format_to_temps(line))
        tempCSV.write(p.format_to_csv(line))

trimmed.close()
templog.close()
tempCSV.close()

g.plot("outputs/" + date + "-temps.csv")