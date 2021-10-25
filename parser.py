import re

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

    temp_pattern = re.compile(" controller: \\d{1,3}\\.\\d{3}  corrected: \\d{1,3}\\.\\d{3}")
    temp_match = temp_pattern.search(line)
    temp_with_labels = temp_match.group()
    temp_with_corrected_labels = temp_with_labels.replace(" controller: ", ",")
    temp = temp_with_corrected_labels.replace("  corrected: ", ",")


    return time + temp + "\n"