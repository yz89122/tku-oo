import math

def sqrt_appr(val, last):
    return (last + val / last) / 2

def main():
    val = float(input('val: '))
    last = 1
    current = 0
    
    while True:
        current = sqrt_appr(val, last)
        print(current)
        if -0.0000001 < (current - last) < 0.0000001:
            break
        last = current

    print(current)
    print('from math.sqrt ' + str(math.sqrt(val)))

if __name__ == '__main__':
    main()
