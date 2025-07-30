code = '''
from collections import deque
def get_neighbors(s):
    i = s.index(0)
    neighbors = []
    for d in [-3, 3, -1, 1]:
        j = i + d
        if 0 <= j < 9 and abs(j//3 - i//3) + abs(j%3 - i%3) == 1:
            n = [*s]
            n[i], n[j] = n[j], n[i]
            neighbors.append(n)
    return neighbors


def bfs_8_puzzle(start, goal):
    if sum(a > b for i, a in enumerate(start[:-1]) for b in start[i+1:] if a and b) % 2:
        return print("Unsolvable")
    q = deque([(start, [])])
    v = {tuple(start)}
    while q:
        s, p = q.popleft()
        if s == goal:
            for i, t in enumerate([start] + p):
                print(f"Step {i + 1}:")
                for j in range(0, 9, 3):
                    print(' '.join(map(str, t[j:j+3])))
                print()
            return
        for n in get_neighbors(s):
            nt = tuple(n)
            if nt not in v:
                q.append((n, p + [n]))
                v.add(nt)
    print("No solution")


print("Enter 3 rows :")
start = sum([[int(x) for x in input(f"Row {i+1}: ").split()] for i in range(3)], [])
goal = [1,2,3,4,5,6,7,8,0]
bfs_8_puzzle(start, goal)
'''

def getCode():
    global code
    print(code)
    