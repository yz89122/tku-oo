import re

regex_contributor = '^From ([a-zA-Z0-9.]+?)@([a-zA-Z0-9]+?(\\.[a-zA-Z0-9]+)+) (... ... .. ..:..:.. ....)$'
regex_commit_version = 'svn commit: r(.....)'

organizations = dict() # org name -> commits versions
contributors = dict() # contributors -> commits versions
commits = dict() # commits versions -> date time

found_contributor = False
contributor = ''
organization = ''
time = ''
version = ''

with open('log.txt') as log_file:
    for line in log_file:
        if not found_contributor:
            m = re.search(regex_contributor, line)
            if m:
                contributor = m.group(1)
                organization = m.group(2)
                time = m.group(4)
                found_contributor = True
        else:
            m = re.search(regex_commit_version, line)
            if m:
                version = m.group(1)
                found_contributor = False
                
                if contributor in contributors:
                    contributors[contributor].append(version)
                else:
                    contributors[contributor] = list([version])
                if organization in organizations:
                    organizations[organization].append(version)
                else:
                    organizations[organization] = list([version])
                commits[version] = time

for k, v in contributors.items():
    print('User', k, 'committed versions:', v) # I'm so lazy
print()
for k, v in organizations.items():
    print('Organization', k, 'committed versions:', v) # :P
print()
for k, v in commits.items():
    print('Version', k, 'created by', v) # :D
