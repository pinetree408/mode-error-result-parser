# -*- coding: utf-8 -*-

import copy
import re
import collections

# path variable for parsed result
file_path = '../result_test.txt'

fr = open(file_path, 'r')
initial_lines = fr.readlines()

lines = []
for line in initial_lines:
    lines.append(line.split('\n')[0])

index_result = []

previous = ''
for i in range(len(lines)):
    line = lines[i]
    splitted = line.split('-')

    log_prog = splitted[2]
    if previous != log_prog:
        previous = log_prog
        index_result.append(i)

range_result = []
for i in range(len(index_result)):
    a = index_result[i]
    b = 0
    if i == len(index_result) - 1:
        b = len(lines) - 1
    else:
        b = index_result[i + 1]
    range_result.append([a, b])

convert_index = []
for item in range_result:
    for i in range(item[0], item[1]):
        if i == (item[1] - 1):
            continue
        rs_splitted = lines[i].split('keyText=')[1]
        sp_splitted = lines[i+1].split('keyText=')[1]
        if rs_splitted == 'Right Meta' and sp_splitted == '␣':
            convert_index.append([i, item[0]])

print len(convert_index)

final = {}
for item in convert_index:
    index = item[0]
    before = lines[index-2].split('keyText=')[1]
    after = lines[index+3].split('keyText=')[1]
    if before == '⌫' or after == '⌫':
        real = 0
        for i in range(item[1], index):
            key_text = lines[i].split('keyText=')[1]
            english = re.compile('[A-Z]')
            if len(english.findall(key_text)) == 1:
                real += 1
	    elif key_text == '␣':
                real = -1
		break
        if real != -1:
	    if item[1] in final.keys():
                updated = copy.deepcopy(final[item[1]])
                updated.append(real)
                del final[item[1]]
                final[item[1]] = updated
            else:
                final[item[1]] = [real]

od = collections.OrderedDict(sorted(final.items()))
print od

initial_length = 0
for key in final.keys():
    initial_length += len(final[key])
print initial_length


first_length = []
for key in final.keys():
    first_length.append(final[key][0])

min = first_length[0]
max = first_length[0]
sum = 0.0

percent_list = [0.0 for i in range(10)]

for item in first_length:
    sum += item
    if min > item:
        min = item
    if max < item:
        max = item
    index = item / 10
    if item != 0 and item % 10 == 0:
        index -= 1
    if index > 9:
        continue
    percent_list[index] += 1

for i in range(len(percent_list)):
    percent_list[i] /= len(first_length)
    percent_list[i] *= 100

print len(first_length)
print min, max, sum/len(first_length)
print percent_list

fr.close()
