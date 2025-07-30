code = '''

def floyd_warshall(g):
    n = len(g)
    d = [[float('inf') if i != j and g[i][j] == 0 else g[i][j] for j in range(n)] for i in range(n)]

    for k in range(n):
        for i in range(n):
            for j in range(n):
                if d[i][k] != float('inf') and d[k][j] != float('inf'):
                    d[i][j] = min(d[i][j], d[i][k] + d[k][j])
    return d

g = [
    [0, 0, 3, 0, 0],
    [0, 0, 10, 4, 0],
    [3, 10, 0, 2, 6],
    [0, 4, 2, 0, 1],
    [0, 0, 6, 1, 0]
]

result = floyd_warshall(g)
print("Shortest distance matrix:")
for row in result:
    print(row)

'''