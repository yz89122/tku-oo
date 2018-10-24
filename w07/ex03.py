lines, upper, lower, digit, space, words, statistic = 0, 0, 0, 0, 0, 0, dict()

with open('text.txt') as input_file:
    for line in input_file:
        lines += 1
        words += len(line.split())
        for letter in line:
            if letter.isspace():
                space += 1
                continue # counting without space char
            elif letter.isupper():
                upper += 1
            elif letter.islower():
                lower += 1
            elif letter.isdigit():
                digit += 1
            l = letter.lower()
            statistic[l] = statistic.get(l, 0) + 1

print(statistic)
print('lines: ', lines)
print('aver words per line: ', words / lines)
print('total upper: ', upper)
print('total lower: ', lower)
print('total digit: ', digit)
print('total space: ', space)

most_freq, most_freq_c = '', 0
for k, v in statistic.items():
    if v > most_freq_c:
        most_freq = k
        most_freq_c = v
print('most freq: ', most_freq)
print('most freq count: ', most_freq_c)
