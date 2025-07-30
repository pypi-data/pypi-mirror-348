def floyd_warshall(graph):
    n = len(graph)
    dist = [[x] * n for _ in range(n)]
   
    for i in range(n):
        for j in range(n):
            dist[i][j] = graph[i][j]
   
    for i in range(n):
        dist[i][i] = 0
       
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][j] > dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    return dist
x = float('inf')
graph = [
    [0, 4, 11],
    [6, 0, 2],
    [3, x, 0]
]


shortest_paths = floyd_warshall(graph)
for row in shortest_paths:
    print(row)


code = '''
def floyd_warshall(graph):
    n = len(graph)
    dist = [[x] * n for _ in range(n)]
   
    for i in range(n):
        for j in range(n):
            dist[i][j] = graph[i][j]
   
    for i in range(n):
        dist[i][i] = 0
       
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][j] > dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    return dist
x = float('inf')
graph = [
    [0, 4, 11],
    [6, 0, 2],
    [3, x, 0]
]


shortest_paths = floyd_warshall(graph)
for row in shortest_paths:
    print(row)
'''

def getCode():
    global code
    print(code)