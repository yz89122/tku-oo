
operations = [
    lambda x, y: x + y,
    lambda x, y: x - y,
    lambda x, y: x * y,
    lambda x, y: x / y
]

op = int(input('op code: '))
x = float(input('x: '))
y = float(input('y: '))

print('result: ' + str(operations[op](x, y)))
