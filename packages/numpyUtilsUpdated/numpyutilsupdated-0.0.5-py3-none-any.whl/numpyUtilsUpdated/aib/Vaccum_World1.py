code="""
flag = False
cnt = 0

def A(d, s):
    global flag
    global cnt
    n = d[s]

    if s == 'A':
        t = 'B'
    else:
        t = 'A'

    if n == 0:
        print('Location', s, 'is Clean.')
    else:
        print('Location', s, 'is Dirty.')
        print('Location', s, 'has been Cleaned.')
        d[s] = 0
        cnt += 1

    if flag:
        print('Environment is Clean.')
    else:
        print('Moving to location', t, '...')
        flag = True
        A(d, t)

import random

d = dict()
d['A'] = random.randrange(0, 2)
d['B'] = random.randrange(0, 2)
s = random.randrange(0, 2)

print(d)

if s:
    print("Vacuum randomly placed at Location B.")
    A(d, 'B')
else:
    print('Vacuum randomly placed at Location A.')
    A(d, 'A')

print(d)
print("Performance Measurement:", cnt)
"""

def getCode():
    global code
    print(code)
    
 