import math

data = list()
total = 0
average = 0
std = 0

while True:
    filename = input('Please specify filename: ')
    try:
        with open(filename) as f_input:
            for line in f_input:
                data.append(int(line))
            break
    except IOError:
        print('cannot read [' + filename + ']')

for n in data:
    total += n

average = total / len(data)
std = math.sqrt(sum((n - average) ** 2 for n in data) / len(data))

def p():
    print('total: ' + str(total))
    print('average: ' + str(average))
    print('standard division: ' + str(std))

def find():
    target = int(input('Which number to find? '))
    count = 0
    for n in data:
        if n == target:
            count += 1
    print('The number ', target, ' is matched for ', count, 'times')

operations = [
    p,
    find
]

while True:
    print('1. calculate total/average/standard division')
    print('2. Find a specific number')
    op = 0
    while True:
        try:
            op = int(input('Op code: '))
            if 1 <= op <= 2:
                break
            else:
                print('Not a choice')
        except:
            print('Non-integer entered!')
    
    operations[op - 1]() # according to the problem :(

    if input('continue (y) or (n): ') != 'y':
        break
