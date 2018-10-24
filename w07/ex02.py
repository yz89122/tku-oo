password = input('Password: ')

print('Include Upper: ', any(letter.isupper() for letter in password))
print('Include Lower: ', any(letter.islower() for letter in password))
print('Include Digit: ', any(letter.isdigit() for letter in password))
print('Len > 10: ', len(password) > 10)
