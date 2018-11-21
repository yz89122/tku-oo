import re

regex_contributor = '^From ([a-zA-Z0-9.]+?)@([a-zA-Z0-9]+?(\\.[a-zA-Z0-9]+)+) (... ... .. ..:..:.. ....)$'
regex_commit_version = 'svn commit: r(.....)'

organizations = dict() # org name -> commits versions
contributors = dict() # contributors -> commits versions
commits = dict() # commits versions -> date time

found_contributor = False

with open('log.txt') as log_file:
    for line in log_file:
        if not found_contributor:
            m = re.search(regex_contributor, line)
            if m:
                contributor, organization, time = m.group(1, 2, 4)
                found_contributor = True
        else:
            m = re.search(regex_commit_version, line)
            if m:
                version = m.group(1)
                found_contributor = False
                
                contributors.setdefault(contributor, list()).append(version)
                organizations.setdefault(organization, list()).append(version)
                commits[version] = time

for k, v in contributors.items():
    print('User', k, 'committed versions:', ' '.join(v))
print()
for k, v in organizations.items():
    print('Organization', k, 'committed versions:', ' '.join(v))
print()
for k, v in commits.items():
    print('Version', k, 'created at', v)
