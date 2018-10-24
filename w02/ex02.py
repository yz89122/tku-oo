selery_ph = float(input('selery per hour: '))
work_hours = int(input('work hours: '))

if work_hours < 40:
    print(selery_ph * work_hours * 0.8)
elif work_hours == 40:
    print(40 * 120)
elif work_hours <= 50:
    print(40 * 120 + (work_hours - 40) * selery_ph * 1.2)
else:
    print((40 * 120) + (10 * selery_ph * 1.2) + (work_hours - 50) * selery_ph * 1.6)
