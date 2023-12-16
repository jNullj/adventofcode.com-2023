import os

f = open(os.path.dirname(__file__) + "/input.txt", "r")
numberLocations = []
symbolsLocation = []
x = 0
y = 0
temp_num_first_indx = -1
temp_num_last_indx = -1
for line in f:
    symbolsLocation.append([])
    line = line[:len(line)-1] # remove \n at end
    for char in line:
        if temp_num_first_indx < 0 and char.isdigit():
            temp_num_first_indx = x
            temp_num_last_indx = x
        elif temp_num_first_indx >= 0 and char.isdigit():
            temp_num_last_indx = x
        elif temp_num_first_indx >= 0 and not char.isdigit():
            numberLocations.append ([
                int(line[temp_num_first_indx:temp_num_last_indx+1]),
                temp_num_first_indx,
                temp_num_last_indx,
                y 
            ])
            temp_num_first_indx = -1
            temp_num_last_indx = -1
        if temp_num_first_indx >= 0 and x == len(line) - 1:
            numberLocations.append ([
                int(line[temp_num_first_indx:temp_num_last_indx+1]),
                temp_num_first_indx,
                temp_num_last_indx,
                y 
            ])
            temp_num_first_indx = -1
            temp_num_last_indx = -1
        if not char.isdigit() and char != '.':
            symbolsLocation[y].append(x)
        x += 1
    x = 0
    y += 1

sum = 0
for [number, x1, x2, y] in numberLocations:
    adjacentFound = False
    symbolSearch = symbolsLocation[y-1] + symbolsLocation[y]
    if y < len(symbolsLocation) - 1:
        symbolSearch += symbolsLocation[y+1]
    for x in symbolSearch:
        if x >= x1 - 1 and x <= x2 + 1 :
            adjacentFound = True
            break

    if adjacentFound:
        sum += number
        continue
    
print(sum)