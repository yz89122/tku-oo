is_c = input('C or F: ') == 'C'
degree = float(input('degree: '))

if is_c:
    print(str(degree * 9 / 5 + 32) + 'F')
else:
    print(str((degree - 32) * 5 / 9) + 'C')
