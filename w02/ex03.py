weight = float(input('weight: '))
height = float(input('height(m): '))
is_male = input('male or female: ') == 'male'
age = int(input('age: '))

bmi = weight / height / height
body_fat = 1.2 * bmi + 0.23 * age - 5.4 - 10.8 * (1 if is_male else 0)

print('BMI: ' + str(bmi))
print('body fat: ' + str(body_fat))

if 18 <= age <= 39:
    if body_fat < 10:
        print('篇瘦')
    elif body_fat < 16:
        print('標準')
    elif body_fat < 21:
        print('偏重')
    elif body_fat < 26:
        print('肥胖')
    else:
        print('嚴重肥胖')
