code="""
def bellman_ford(V, edges): 
    dist = [float('inf')] * V 
    dist[0] = 0 
    for _ in range(V - 1): 
        for u, v, w in edges: 
            if dist[u] != float('inf') and dist[u] + w < dist[v]: 
                dist[v] = dist[u] + w 
    for u, v, w in edges: 
        if dist[u] != float('inf') and dist[u] + w < dist[v]: 
            print("Graph contains negative cycles.") 
            return 
    print("Vertex Distance") 
    for i, d in enumerate(dist): 
        print(f"{i} {d}") 

V = int(input("Enter number of vertices: ")) 
E = int(input("Enter number of edges: ")) 
edges = [] 
print("Enter edges (u, v, w):") 
for _ in range(E): 
    edges.append(list(map(int, input().split()))) 
bellman_ford(V, edges)
"""
