import re
import datetime as dt

initial_time = 0

def set_init_time(line):
    rawtime = line[11:23]
    formatted_time = rawtime.replace(",",".")
    global initial_time
    initial_time = convert_time_to_seconds(formatted_time)


def convert_time_to_seconds(time):
    h, m, s = time.split(":")
    return float(h)*3600 + float(m)*60 + float(s)

def is_not_fluff(line):
    # return false if contains any of these 4 keywords, 
    remove_if_contains = ["Sending", "Writing", "Received", "Raising"]
    for key in remove_if_contains:
        key_as_regex = re.compile(key)
        found = key_as_regex.search(line)
        if not found:
            continue
        else: 
            return False
    # return false if line is too short
    return len(line) > 8

def contains_temp_data_points(line):
    pattern = re.compile("controller: \\d{1,3}\\.\\d{3}  corrected: \\d{1,3}\\.\\d{3}")
    found = pattern.search(line)
    if not found:
        return False
    else: 
        return True

def format_to_temps(line):
    time_pattern = re.compile("\\d\\d:\\d\\d:\\d\\d,\\d{3}")
    time_match = time_pattern.search(line)
    time_with_comma = time_match.group()
    time = time_with_comma.replace(",", ".")

    temp_pattern = re.compile(" controller: \\d{1,3}\\.\\d{3}  corrected: \\d{1,3}\\.\\d{3}")
    temp_match = temp_pattern.search(line)
    temp = temp_match.group()

    return time + " " + temp + "\n"

def format_to_csv(line):
    time_pattern = re.compile("\\d\\d:\\d\\d:\\d\\d,\\d{3}")
    time_match = time_pattern.search(line)
    time_with_comma = time_match.group()
    time = time_with_comma.replace(",", ".")
    
    seconds = convert_time_to_seconds(time) - initial_time

    uncorr_pattern = re.compile(" controller: \\d{1,3}\\.\\d{3}")
    uncorr_match = uncorr_pattern.search(line)
    uncorrected_temp_labelled = uncorr_match.group()
    uncorrected_temp = uncorrected_temp_labelled.replace(" controller: ","")

    corr_pattern = re.compile("  corrected: \\d{1,3}\\.\\d{3}")
    corr_match = corr_pattern.search(line)
    corr_temp_labelled = corr_match.group()
    corrected_temp = corr_temp_labelled.replace("  corrected: ","")

    return time + "," + str(seconds) + "," +  uncorrected_temp + "," + corrected_temp + "\n"