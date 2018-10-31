a = ord('a')
z = ord('z')

while True:
    op = input('(1) encode, (2) decode: ')
    if op == '1':
        offset = int(input('encode offset: '))
        s = input('encode string: ')
        for i in range(len(s)):
            c = s[i]
            if a <= ord(c) <= z:
                c = chr((ord(c) - a + offset) % 26 + a)
                print(c, end='')
            else:
                print(c, end='')
    else:
        offset = int(input('decode offset: '))
        s = input('decode string: ')
        for i in range(len(s)):
            c = s[i]
            if a <= ord(c) <= z:
                c = chr((ord(c) - a - offset) % 26 + a)
                print(c, end='')
            else:
                print(c, end='')
    print()
    cont = input('y or n: ')
    if cont != 'y':
        break