file_path = '../result_test.txt'

fr = open(file_path, 'r')
lines = fr.readlines()

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
        b = index_result[i + 1] - 1
    range_result.append([a, b])

print range_result

fr.close()
