def find(parent, u):
    while parent[u] != u:
        u = parent[u]
    return u

def union(parent, u, v):
    root_u = find(parent, u)
    root_v = find(parent, v)
    
    if root_u != root_v:
        parent[root_v] = root_u

def kruskal(graph):
    edges = []
    V = len(graph)

    # Create a list of edges with their weights
    for u in range(V):
        for v in range(u + 1, V):
            if graph[u][v] != 0:
                edges.append([u, v, graph[u][v]])

    # Sort the edges by weight
    edges.sort(key=lambda x: x[2])

    # Initialize parent list (each node is its own parent)
    parent = list(range(V))
    mst_edges = []

    # Process each edge
    for u, v, weight in edges:
        if find(parent, u) != find(parent, v):
            union(parent, u, v)
            mst_edges.append([u, v, weight])

    # Display the MST edges
    for u, v, weight in mst_edges:
        print(f"Edge: {u} - {v}, Weight: {weight}")

# Example usage:
graph = [
    [0, 2, 0, 6, 0],
    [2, 0, 3, 8, 5],
    [0, 3, 0, 0, 7],
    [6, 8, 0, 0, 9],
    [0, 5, 7, 9, 0]
]

kruskal(graph)


code = '''
def find(parent, u):
    while parent[u] != u:
        u = parent[u]
    return u

def union(parent, u, v):
    root_u = find(parent, u)
    root_v = find(parent, v)
    
    if root_u != root_v:
        parent[root_v] = root_u

def kruskal(graph):
    edges = []
    V = len(graph)

    # Create a list of edges with their weights
    for u in range(V):
        for v in range(u + 1, V):
            if graph[u][v] != 0:
                edges.append([u, v, graph[u][v]])

    # Sort the edges by weight
    edges.sort(key=lambda x: x[2])

    # Initialize parent list (each node is its own parent)
    parent = list(range(V))
    mst_edges = []

    # Process each edge
    for u, v, weight in edges:
        if find(parent, u) != find(parent, v):
            union(parent, u, v)
            mst_edges.append([u, v, weight])

    # Display the MST edges
    for u, v, weight in mst_edges:
        print(f"Edge: {u} - {v}, Weight: {weight}")

# Example usage:
graph = [
    [0, 2, 0, 6, 0],
    [2, 0, 3, 8, 5],
    [0, 3, 0, 0, 7],
    [6, 8, 0, 0, 9],
    [0, 5, 7, 9, 0]
]

kruskal(graph)

'''

def getCode():
    global code
    print(code)
    