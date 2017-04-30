# -*- coding: utf-8 -*-

import copy
import re
import collections

# path variable for parsed result
file_path = '../prevent_recover/result.txt'

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

    log_prog = splitted[3]
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

convert = {}
convert_index = []
for item in range_result:
    for i in range(item[0], item[1]):
        if i == (item[1] - 1):
            continue
        rs_splitted = lines[i].split('-')[1]
        #sp_splitted = lines[i+1].split('-')[1]
        #if rs_splitted == 'Right Meta' and sp_splitted == '␣':
	if rs_splitted == '가타카나':
            date = lines[i].split('-')[0].split(' ')[2]
            if date in convert.keys():
                updated = convert[date]
                del convert[date]
                convert[date] = updated + 1
            else:
                convert[date] = 1

            convert_index.append([i, item[0]])

# number of korean english switching key used
print len(convert_index)
print convert

mode_error = {}
total_mode_error = 0
for item in convert_index:
    index = item[0]
    #before = lines[index-2].split('keyText=')[1]
    #after = lines[index+3].split('keyText=')[1]

    before = lines[index-1].split('-')[1]
    after = lines[index+1].split('-')[1]

    #if before == '⌫' or after == '⌫':
    if before == 'Backspace' or after == 'Backspace':
        date = lines[index].split('-')[0].split(' ')[2]
        if date in mode_error.keys():
            updated = mode_error[date]
            del mode_error[date]
            mode_error[date] = updated + 1
        else:
            mode_error[date] = 1
        total_mode_error += 1

print total_mode_error
print mode_error

'''
final = {}
for item in convert_index:
    index = item[0]
    #before = lines[index-2].split('keyText=')[1]
    #after = lines[index+3].split('keyText=')[1]

    before = lines[index-1].split('-')[1]
    after = lines[index+1].split('-')[1]

    #if before == '⌫' or after == '⌫':
    if before == 'Backspace' or after == 'Backspace':
        real = 0
        for i in range(item[1], index):
            #key_text = lines[i].split('keyText=')[1]
            key_text = lines[i].split('-')[1]
            english = re.compile('[A-Z]')
            if len(english.findall(key_text)) == 1:
                real += 1
	    #elif key_text == '␣':
            elif key_text == 'Backspace':
                real = 0
	    	#break
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
print final


initial_length = 0
for key in final.keys():
    initial_length += len(final[key])
print initial_length


first_length = []
for key in final.keys():
    for i in range(len(final[key])):
        first_length.append(final[key][i])

min = first_length[0]
max = first_length[0]
sum = 0.0

print first_length

percent_list = [0.0 for i in range(50)]

for item in first_length:
    sum += item
    if min > item:
        min = item
    if max < item:
        max = item
    index = item / 10
    if item != 0 and item % 10 == 0:
        index -= 1
    #if index > 9:
    #    continue
    #print item, index
    percent_list[index] += 1

for i in range(len(percent_list)):
    percent_list[i] /= len(first_length)
    percent_list[i] *= 100

print len(first_length)
print min, max, sum/len(first_length)
for i in range(len(percent_list)):
    print percent_list[i]
'''
fr.close()
