import collections

teams = collections.defaultdict(list)
skip = set({1904, 1994})
year = 1903

with open('WorldSeriesWinners.txt') as input_file:
    for team in (line.strip() for line in input_file):
        while year in skip:
            year += 1
        teams[team].append(year)
        year += 1

for k, v in teams.items():
    print(k + '\t' * (4 - len(k) // 8), 'wins', len(v), 'times')

op = input('input 1 or 2: ')
if op == '1':
    team = input('team: ')
    if team in teams:
        print(team+ '\t' * (4 - len(k) // 8), 'wins', len(teams[team]), 'times')
        print(' '.join((str(year) for year in teams[team])))
    else:
        print(':(')
elif op == '2':
    t = int(input('win times: '))
    for k, v in teams.items():
        if len(v) == t:
            print(k + '\t' * (4 - len(k) // 8), 'wins', len(v), 'times')
