import random

LIMIT = 5

def guessing(target, guess): # according to the problem
    if target > guess:
        return 1
    elif target == guess:
        return 0
    return -1

def main():
    cont = True
    while cont:
        low = 1
        high = 100
        target = random.randint(low, high)
        for _ in range(LIMIT):
            guess = int(input('Guess a number from ' + str(low) + ' to ' + str(high) + ': '))
            result = guessing(target, guess)
            if result == 1:
                print('Too low!')
                if low < guess:
                    low = guess
            elif result == -1:
                print('Too high!')
                if high > guess:
                    high = guess
            else:
                if input('You passwd, next game? ') != 'y':
                    cont = False
                break
        else:
            if input('Achieve limit, try again? ') != 'y':
                cont = False

if __name__ == '__main__':
    main()
