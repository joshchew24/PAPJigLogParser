from ast import parse
import sys
import re
import log_parser as p
import grapher as g

global path
global file
global command
global date

def main():
    global path
    global command
    if len(sys.argv) != 3:
        exit("Usage: \'main.py <parse/graph/process> <path>/\'\narg1 is the path/filename of .log path to be parsed.")
    command = sys.argv[1]
    path = sys.argv[2]
    
    processCommand()


def processCommand():
    global path
    global command
    
    commandPattern = re.compile("parse|graph|process")
    commandMatch = commandPattern.search(command)
    if not commandMatch:
        exit("\'" + command + "\' is not one of the valid commands: \'parse\', \'graph\', \'process\'")

    readFile()

    if (command == "parse"):
        parse()
    elif (command == "graph"):
        graph()
    elif (command == "process"):
        parse()
        graph()


def readFile():
    global path
    global file
    global date
    accept_csv = (command == "graph")
    
    pattern = re.compile("(app_20(1|2)\\d(0|1)\\d[0-3]\\d\\.log)%s" %("|(20(1|2)\\d(0|1)\\d[0-3]\\d\\-temps\\.csv)" if accept_csv else ""))
    m = pattern.search(path)

    if not m:
        exit("Error: filename should be of format \'app_YYYYMMDD.log\'. Can also graph files of format \'YYYYMMDD-temps.csv\'")

    filename = m.group()

    # useless check, matched regex will guarantee length.
    # if (len(filename) != 16): 
    #     exit("Error: filename should be of format \'app_YYYYMMDD.log\'")

    try:
        file = open(path, "r")
    except FileNotFoundError as e:
        quit("Error: File not found. Verify it exists in the specified directory. If graphing .log files, parse them prior to graphing.")

    date = filename[4:12]


def parse():
    lines = file.readlines()
    file.close()
    
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

    # file.close()
    trimmed.close()
    templog.close()
    tempCSV.close()


def graph():
    g.plot("outputs/" + date + "-temps.csv")


if __name__ == "__main__":
    main()