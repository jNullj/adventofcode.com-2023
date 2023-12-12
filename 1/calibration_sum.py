import re

def numbers_from_strings(string: str) -> list[int]:
    regex = "\d"
    return re.findall(regex, string)

def extract_calib_val(string: str) -> int:
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
