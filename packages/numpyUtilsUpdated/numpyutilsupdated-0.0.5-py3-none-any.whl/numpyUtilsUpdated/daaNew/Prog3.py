code = '''

n = 5
graph = [
    [0, 0, 3, 0, 0],
    [0, 0, 10, 4, 0],
    [3, 10, 0, 2, 6],
    [0, 4, 2, 0, 1],
    [0, 0, 6, 1, 0]
]

selected = [True] + [False] * (n - 1)
edges = 0
cost = 0

print("Edges in MST:")
while edges < n - 1:
    min_edge = (float('inf'), -1, -1)
    for i in range(n):
        if selected[i]:
            for j in range(n):
                if not selected[j] and 0 < graph[i][j] < min_edge[0]:
                    min_edge = (graph[i][j], i, j)

    w, u, v = min_edge
    print(f"{u} - {v} : {w}")
    selected[v] = True
    cost += w
    edges += 1

print(f"\nTotal Cost of MST: {cost}")

'''