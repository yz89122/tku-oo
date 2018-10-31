input_str = input('Please input a string: ')
statistic = dict()

for letter in input_str:
    if letter in statistic.keys():
        statistic[letter] += 1
    else:
        statistic[letter] = 1

print('count results are as below')
for k, v in statistic.items():
    print('The char ', k, ' appear ', v, ' times')
