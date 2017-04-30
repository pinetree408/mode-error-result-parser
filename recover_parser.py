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

convert_index = []
for item in range_result:
    for i in range(item[0], item[1]):
        if i == (item[1] - 1):
            continue
        rs_splitted = lines[i].split('-')[1]
	if rs_splitted == '가타카나':
            convert_index.append([i, item[0]])

print len(convert_index)


full = 0
recover = 0

learning_curve = {}


final = {}
for item in convert_index:
    index = item[0]
    before = lines[index-1].split('-')[1]
    after = lines[index+1].split('-')[1]

    full_learn = 0
    recover_learn = 0

    if before == 'Backspace' or after == 'Backspace':

        full += 1
        real = 0
        for i in range(item[1], index):
            key_text = lines[i].split('-')[1]
            english = re.compile('[A-Z]')
            if len(english.findall(key_text)) == 1:
                real += 1
	    elif key_text == 'Space':
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
                full_learn = 1

        #full_learn = 1

    if after == 'Backspace':
        recover += 1
	recover_learn = 1

    date_set = lines[index].split('-')[0].split(' ')[3].split(':')[0:2]
    #date = lines[index].split('-')[0].split(' ')[2]
    date = lines[index].split('-')[0].split(' ')[2] + '-' + ':'.join(date_set)
    #date = ':'.join(date_set)

    if date in learning_curve.keys():
        updated = copy.deepcopy(learning_curve[date])
	remake = {
	    'full': updated['full'] + full_learn, 
	    'recover': updated['recover'] + recover_learn
	}
	del learning_curve[date]
	learning_curve[date] = remake
    else:
        remake = {
	    'full': full_learn, 
	    'recover': recover_learn
	}
	learning_curve[date] = remake


#print learning_curve

'''
for key in learning_curve.keys():
    date = key.split('-')[0]
    time = key.split('-')[1]
    full = learning_curve[key]['full']
    recover = learning_curve[key]['recover']

    if full != 0:
        percent = (recover / (full * 1.0)) * 100
        print date + ' ' + time + ' ' + str(percent) + ' ' + str(full) + ' ' + str(recover)
'''

reorder = {}
for key in learning_curve.keys():
    date = key.split('-')[0]
    full = learning_curve[key]['full']
    recover = learning_curve[key]['recover']
    if date in reorder.keys():
        updated = copy.deepcopy(reorder[date])
	remake = {
	    'full': updated['full'] + full, 
	    'recover': updated['recover'] + recover
	}
	del reorder[date]
	reorder[date] = remake
    else:
        remake = {
	    'full': full, 
	    'recover': recover
	}
	reorder[date] = remake

print reorder

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
