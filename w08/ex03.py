a = ord('a')
z = ord('z')

while True:
    op = int(input('(1) encode, (2) decode: '))

    offset = int(input('encode/decode offset: ')) * \
            1 if op & 1 else -1
    s = input('encode/decode string: ')
    
    for i in range(len(s)):
        c = s[i]
        if a <= ord(c) <= z:
            c = chr((ord(c) - a + offset) % 26 + a)
            print(c, end='')
        else:
            print(c, end='')
    print()

    cont = input('y or n: ')
    if cont != 'y':
        break
