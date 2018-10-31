teams = dict()
skip = set({1904, 1994})
year = 1903

with open('WorldSeriesWinners.txt') as input_file:
    for line in input_file:
        team = line.strip()
        if year in skip:
            year += 1
        if team in teams:
            teams[team]['win_years'].append(year)
            teams[team]['count'] += 1
        else:
            teams[team] = dict(
                {
                    'win_years': list([year]),
                    'count': 1
                }
            )
        year += 1

for k, v in teams.items():
    print(k, ' wins ', v['count'], ' times')

op = input('input 1 or 2: ')
if op == '1':
    team = input('team: ')
    if team in teams.keys():
        print(team, ' wins ', teams[team]['count'], ' times')
        for y in teams[team]['win_years']:
            print(y)
    else:
        print(':(')
elif op == '2':
    if team in teams.keys():
        t = int(input('win times: '))
        for k, v in teams.items():
            if v['count'] == t:
                print(k, ' wins ', v['count'], ' times')
    else:
        print(':(')
