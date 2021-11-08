from ast import parse
import sys
import re
import log_parser as p
import grapher as g

global path
global file
global command
global date
global commands 
commands = ["parse","graph","process","help","exit","q"]

def main():
    # global path
    # global command
    if len(sys.argv) == 1:
        promptCommandInput()
        promptFileInput()
        executeCommand()
    # elif len(sys.argv) != 3:
    #     exit("Usage: \'main.py <parse/graph/process> <path>/\'\narg1 is the path/filename of .log path to be parsed.")
    # command = sys.argv[1]
    # path = sys.argv[2]
    
    # parseCommand()

def promptCommandInput():
    global command
    command = input("Enter function... ")
    parseCommand()

def parseCommand():
    patternString = getCommandStrings()
    commandPattern = re.compile(patternString)
    commandMatch = commandPattern.search(command)
    if not commandMatch:
        print("\'" + command + "\' is not one of the valid commands: ")
        print(*commands, sep = ', ')
        promptCommandInput()
    if (command == "help"): 
        printHelp()
        promptCommandInput()
    if (command == "exit" or command == "q"):
        exit("Exiting...")

def promptFileInput():
    global path
    path = input("Enter file or directory to " + command + "... ")
    parseFile()
    
def parseFile():
    global file
    global date
    isGraphing = command == "graph"
    
    pattern = re.compile("(20(1|2)\\d(0|1)\\d[0-3]\\d\\-temps\\.csv)" if isGraphing else "(app_20(1|2)\\d(0|1)\\d[0-3]\\d\\.log)")
    # pattern = re.compile("(app_20(1|2)\\d(0|1)\\d[0-3]\\d\\.log)%s" %("|(20(1|2)\\d(0|1)\\d[0-3]\\d\\-temps\\.csv)" if accept_csv else ""))
    m = pattern.search(path)
    
    if not m:
        print("Error: filename should be of format \'YYYYMMDD-temps.csv\'" if isGraphing else "Error: filename should be of format \'app_YYYYMMDD.log\'.")
        promptFileInput()

    filename = m.group()
    try:
        file = open(path, "r")
    except FileNotFoundError as e:
        print("Exiting: File not found. Verify it exists in the specified directory. If graphing .log files, parse them prior to graphing.")
        promptFileInput()

    date = filename[0:8] if isGraphing else filename[4:12]
    print(date)

def printHelp():
    print("Parse:   reads log file and generates three new versions - trimmed, and temperature data in .log and .csv format.")
    print("Graph:   graph a .csv file containing temperature data.")
    print("Process: parse then graph")
    # print("Parse: read log file and generate three new versions - trimmed, and temperature data in readable format and .csv format.")
    # print("Parse: read log file and generate three new versions - trimmed, and temperature data in readable format and .csv format.")

def getCommandStrings():
    patternString = commands[0]
    first = True

    for s in commands:
        if first:
            first = False
            continue
        patternString += "|" + s

    return patternString



def executeCommand():
    if (command == "parse"):
        parse()
    elif (command == "graph"):
        graph()
    elif (command == "process"):
        parse()
        graph()




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