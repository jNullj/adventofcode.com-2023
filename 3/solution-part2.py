import os

f = open(os.path.dirname(__file__) + "/input.txt", "r")
numberLocations = []
symbolsLocation = []
x = 0
y = 0
temp_num_first_indx = -1
temp_num_last_indx = -1
for line in f:
    numberLocations.append([])
    line = line[:len(line)-1] # remove \n at end
    for char in line:
        if temp_num_first_indx < 0 and char.isdigit():
            temp_num_first_indx = x
            temp_num_last_indx = x
        elif temp_num_first_indx >= 0 and char.isdigit():
            temp_num_last_indx = x
        elif temp_num_first_indx >= 0 and not char.isdigit():
            numberLocations[y].append([
                int(line[temp_num_first_indx:temp_num_last_indx+1]),
                temp_num_first_indx,
                temp_num_last_indx
            ])
            temp_num_first_indx = -1
            temp_num_last_indx = -1
        if temp_num_first_indx >= 0 and x == len(line) - 1:
            numberLocations[y].append ([
                int(line[temp_num_first_indx:temp_num_last_indx+1]),
                temp_num_first_indx,
                temp_num_last_indx
            ])
            temp_num_first_indx = -1
            temp_num_last_indx = -1
        if not char.isdigit() and char != '.':
            symbolsLocation.append([x, y, char])
        x += 1
    x = 0
    y += 1

sum = 0
for [x, y, char] in symbolsLocation:
    if char != '*':
        continue
    adjacentNumbers = []
    searchLines = numberLocations[y-1] + numberLocations[y]
    if y < len(numberLocations) - 1:
        searchLines += numberLocations[y+1]
    for [number, x1, x2] in searchLines:
        if x >= x1 - 1 and x <= x2 + 1:
            adjacentNumbers.append(number)
    if len(adjacentNumbers) == 2:
        sum += adjacentNumbers[0] * adjacentNumbers[1]

print(sum)