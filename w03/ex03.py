width = int(input(''))
for i in range(width // 2):
  print(' ' * i)
for i, j in ((i, j) for i in range(width) for j in range(width)):
  print((' ' if i + j < width // 2 or i - j > width // 2 or (i + j) > (width + width // 2 - 1) or j - i > width // 2 else '*') + ('\n' if j == width - 1 else ''), end='')
