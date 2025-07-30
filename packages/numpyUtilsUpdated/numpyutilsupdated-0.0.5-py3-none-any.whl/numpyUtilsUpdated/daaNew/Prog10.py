code = '''

x = float('inf')

v = int(input("Enter number of vertices: "))
e = int(input("Enter number of edges: "))
print("Enter edges (u, v, w):")
edges = [tuple(map(int, input().split())) for _ in range(e)]

dist = [x] * v
dist[0] = 0 

for _ in range(v - 1):
    for u, vtx, w in edges:
        if dist[u] + w < dist[vtx]:
            dist[vtx] = dist[u] + w

if any(dist[u] + w < dist[vtx] for u, vtx, w in edges):
    print("Graph contains a negative weight cycle!")
else:
    print("Vertex Distance")
    for i, d in enumerate(dist):
        print(i, d if d != x else "INF")

'''