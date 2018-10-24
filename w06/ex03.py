data = list()

with open('USPopulation.txt', 'r') as f_input:
    for line in f_input:
        data.append(int(line))

max = 0
max_y = 0
min = 999999999999
min_y = 0
c = 0
last = 0

for i, n in enumerate(data):
    c += n
    if i == 0:
        last = n
        continue
    diff = n - last
    if diff > max:
        max = diff
        max_y = i - 1
        max_c = c
    if diff < min:
        min = diff
        min_y = i - 1
        min_c = c
    last = n

print(max_y + 1950, '-' , max_y + 1951)
print(min_y + 1950, '-', min_y + 1951)
print(c)
