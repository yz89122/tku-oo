input_str = input('input: ')

input_list = list()
last = ''
for letter in input_str:
    if last != letter:
        last = letter
        input_list.append(letter)

print(input_list)
