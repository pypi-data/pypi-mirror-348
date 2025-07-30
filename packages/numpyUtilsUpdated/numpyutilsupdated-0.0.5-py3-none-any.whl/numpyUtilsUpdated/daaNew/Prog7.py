code = '''

import heapq

def dijkstra(g, s):
    n = len(g)
    d = [float('inf')]*n
    d[s] = 0
    h = [(0, s)]
    while h:
        du, u = heapq.heappop(h)
        for v, w in enumerate(g[u]):
           if w and du + w < d[v]:
               d[v] = du + w
               heapq.heappush(h, (d[v], v))
    return d

graph = [
    [0, 0, 3, 0, 0],
    [0, 0, 10, 4, 0],
    [3, 10, 0, 2, 6],
    [0, 4, 2, 0, 1],
    [0, 0, 6, 1, 0]
]

s = 0
res = dijkstra(graph, s)

print(f"\nShortest distances from {s}:")
for i, d in enumerate(res):
    print(f"{i + 1} - {d}")

'''