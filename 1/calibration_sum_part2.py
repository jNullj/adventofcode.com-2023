import re
import math

def numbers_from_strings(string: str) -> list[int]:
    regex = "\d"
    return re.findall(regex, string)

def numer_name_to_char(string: str) -> str:
    decoder = {
        'one': '1',
        'two': '2',
        'three': '3',
        'four': '4',
        'five': '5',
        'six': '6',
        'seven': '7',
        'eight': '8',
        'nine': '9'
    }
    smallest_idx = {'name': '', 'index': math.inf}
    highest_idx = {'name': '', 'index': 0}
    for name in decoder:
        first_index = string.find(name)
        last_index = string.rfind(name)
        if first_index == -1:
            continue
        if first_index < smallest_idx['index']:
            smallest_idx['index'] = first_index
            smallest_idx['name'] = name
        if last_index > highest_idx['index']:
            highest_idx['index'] = last_index
            highest_idx['name'] = name
    if smallest_idx['index'] == math.inf:
        return string
    string = decoder[smallest_idx['name']].join([
        string[:smallest_idx['index']],
        string[smallest_idx['index']:]
    ])
    if smallest_idx['index'] == highest_idx['index']:
        return string
    string = decoder[highest_idx['name']].join([
        string[:highest_idx['index']+1],
        string[highest_idx['index']+1:]
    ])
    return string

def extract_calib_val(string: str) -> int:
    string = string[:-1] # remove newline break
    string = numer_name_to_char(string)
    numers = numbers_from_strings(string)
    first_num = numers[0]
    last_num = numers[-1]
    calibration_val = first_num + last_num
    return int(calibration_val)

f = open("input.txt", "r")
sum = 0
for line in f:
    cal_val = extract_calib_val(line)
    sum += cal_val

print(sum)
