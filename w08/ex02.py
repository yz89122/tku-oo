teams = dict()
skip = set({1904, 1994})
year = 1903

with open('WorldSeriesWinners.txt') as input_file:
    for team in (line.strip() for line in input_file):
        if year in skip:
            year += 1
        if team in teams:
            teams[team].append(year)
        else:
            teams[team] = list([year])
        year += 1

for k, v in teams.items():
    print(k + '\t' * (4 - len(k) // 8), 'wins', len(v), 'times')

op = input('input 1 or 2: ')
if op == '1':
    team = input('team: ')
    if team in teams:
        print(team+ '\t' * (4 - len(k) // 8), 'wins', len(teams[team]), 'times')
        for y in teams[team]:
            print(y)
    else:
        print(':(')
elif op == '2':
    t = int(input('win times: '))
    for k, v in teams.items():
        if len(v) == t:
            print(k + '\t' * (4 - len(k) // 8), 'wins', len(v), 'times')
