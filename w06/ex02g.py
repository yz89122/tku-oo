import random

filename = input('Please specify filename: ')
amount = 0

while True:
    try:
        amount = int(input('Please enter amount of data: '))
        if amount < 0:
            print('should be positive')
            continue
        break
    except:
        print('Non-integer entered!')

with open(filename, 'w') as output:
    for _ in range(amount):
        output.write(str(random.randint(0, 500)) + '\n')
