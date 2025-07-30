code="""
def prims(graph): 
    V = len(graph) 
    selected = [False] * V 
    selected[0] = True 
    edges = 0 
    cost = 0 
    while edges < V - 1: 
        min_edge = float('inf') 
        x, y = 0, 0 
        for i in range(V): 
            if selected[i]: 
                for j in range(V): 
                    if not selected[j] and graph[i][j]: 
                        if min_edge > graph[i][j]: 
                            min_edge = graph[i][j] 
                            x, y = i, j 
        print(f"{x} - {y}: {graph[x][y]}") 
        cost += graph[x][y] 
        selected[y] = True 
        edges += 1 
    print(f"Minimum Cost = {cost}") 

V = int(input("Enter number of vertices: ")) 
graph = [] 
print("Enter the adjacency matrix:") 
for _ in range(V): 
    row = list(map(int, input().split())) 
    graph.append(row) 
prims(graph)
"""
