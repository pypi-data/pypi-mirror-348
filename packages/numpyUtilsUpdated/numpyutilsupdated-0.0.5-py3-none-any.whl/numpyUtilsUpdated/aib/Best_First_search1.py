code="""
import heapq

path = []
q = []
vis = []

d = {
    'a': [['z', 75, 374], ['t', 118, 329], ['s', 140, 253]],
    'z': [['a', 75, 366], ['o', 71, 380]],
    'o': [['z', 71, 374], ['s', 151, 253]],
    's': [['a', 140, 366], ['f', 99, 176], ['r', 80, 193]],
    't': [['a', 118, 366], ['l', 111, 244]],
    'l': [['t', 111, 329], ['m', 70, 241]],
    'm': [['l', 70, 244], ['d', 75, 242]],
    'd': [['c', 120, 160], ['m', 75, 241]],
    'c': [['d', 120, 242], ['r', 146, 193], ['p', 138, 100]],
    'r': [['s', 80, 253], ['c', 146, 160], ['p', 97, 100]],
    'p': [['r', 97, 193], ['b', 101, 0], ['c', 138, 160]],
    'f': [['s', 99, 253], ['b', 211, 0]],
}

h = {
    'a': 366, 'z': 374, 'o': 380, 's': 253, 't': 329, 'l': 244,
    'm': 241, 'd': 242, 'c': 160, 'r': 193, 'p': 100, 'f': 176, 'b': 0
}

def AStar(src, dest):
    heapq.heappush(q, (h[src], src, 0, -1))
    while q:
        _, cur, g, parent = heapq.heappop(q)
        vis.append([cur, g, parent])

        if cur == dest:
            print(f"Path Cost: {g}")
            while cur != -1:
                for i, j, k in vis:
                    if cur == i:
                        cur = k
                        path.append(i)
            return

        for neighbor, edge_cost, _ in d[cur]:
            heapq.heappush(q, (g + edge_cost + h[neighbor], neighbor, g + edge_cost, cur))

start = input("Enter the start point: ")
dest = input('Enter the destination: ')
AStar(start, dest)

print(f"Path: {path[::-1]}")
"""

def getCode():
    global code
    print(code)
    
    