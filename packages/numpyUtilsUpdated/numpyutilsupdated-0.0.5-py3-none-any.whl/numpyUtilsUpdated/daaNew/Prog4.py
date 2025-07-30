code = '''

n = 5
graph = [
    [0, 0, 3, 0, 0],
    [0, 0, 10, 4, 0],
    [3, 10, 0, 2, 6],
    [0, 4, 2, 0, 1],
    [0, 0, 6, 1, 0]
]

edges = sorted((graph[i][j]) for i in range(n) for j in range(i + 1, n) if graph[i][j])
cost = 0
parent = list(range(n))

def find(v):
    if parent[v] != v:
        parent[v] = find(parent[v])
    return parent[v]

print("Edges in MST: ")
for w, u, v in edges:
    ru, rv = find(u), find(v)
    if ru != rv:
        parent[ru] = rv
        cost += w
        print(f"{u} - {v} : {w}")
        if parent.count(parent[0]) == n:
            break
print(f"\nTotal Cost of MST: {cost}")

'''