width = int(input('Please enter a value: '))

if width <= 0:
  quit()

for i in range(width, 1, -1):
  print('*' * i)

for i in range(1, width + 1):
  print('*' * i)
