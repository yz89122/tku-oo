time = int(input())

h = time // 60 // 60
m = time % (60 * 60) // 60
s = time % 60

print('{0:02}:{1:02}:{2:02}'.format(h, m, s))
