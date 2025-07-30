code="""
def floyd_warshall(graph): 
    V = len(graph) 
    dist = [row[:] for row in graph] 
    for k in range(V): 
        for i in range(V): 
            for j in range(V): 
                dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j]) 
    print("Shortest distances between every pair of vertices:") 
    for row in dist: 
        print(' '.join(map(str, row))) 

V = int(input("Enter number of vertices: ")) 
graph = [] 
print("Enter the cost matrix:") 
for _ in range(V): 
    row = list(map(int, input().split())) 
    for j in range(V): 
        if row[j] == 0 and _ != j: 
            row[j] = float('inf') 
    graph.append(row) 
floyd_warshall(graph)
"""