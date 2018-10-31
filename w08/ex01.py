statistic = dict()

for letter in input('Please input a string: '):
    statistic[letter] = statistic.get(letter, 0) + 1

print('count results are as below')
for k, v in statistic.items():
    print('The char ', k, ' appear ', v, ' times')
