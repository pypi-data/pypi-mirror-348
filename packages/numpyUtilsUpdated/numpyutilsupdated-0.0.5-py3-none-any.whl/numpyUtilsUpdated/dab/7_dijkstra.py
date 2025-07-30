code="""
def dijkstra(graph, start): 
    V = len(graph) 
    dist = [float('inf')] * V 
    dist[start] = 0 
    visited = [False] * V 
    for _ in range(V - 1): 
        min_dist = float('inf') 
        u = -1 
        for v in range(V): 
            if not visited[v] and dist[v] < min_dist: 
                min_dist = dist[v] 
                u = v 
        if u == -1: 
            break 
        visited[u] = True 
        for v in range(V): 
            if graph[u][v] and dist[u] + graph[u][v] < dist[v]: 
                dist[v] = dist[u] + graph[u][v] 
    print("Vertex Cost") 
    for i, d in enumerate(dist): 
        print(f"{i + 1} {d}") 

V = int(input("Enter number of vertices: ")) 
graph = [] 
print("Enter the adjacency matrix:") 
for _ in range(V): 
    graph.append(list(map(int, input().split()))) 
dijkstra(graph, 0)
"""