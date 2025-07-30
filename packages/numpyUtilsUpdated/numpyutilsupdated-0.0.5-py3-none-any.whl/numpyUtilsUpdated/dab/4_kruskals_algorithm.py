code="""
def kruskals(n, edges): 
    parent = list(range(n)) 
    def find(i): 
        if parent[i] == i: 
            return i 
        return find(parent[i]) 
    def union(i, j): 
        root_i, root_j = find(i), find(j) 
        if root_i != root_j: 
            parent[root_i] = root_j 
            return True 
        return False 
    edges.sort(key=lambda x: x[2]) 
    cost = 0 
    for u, v, w in edges: 
        if union(u, v): 
            print(f"{u} - {v}: {w}") 
            cost += w 
    print(f"Minimum cost = {cost}") 

n = int(input("Enter number of vertices: ")) 
edges = [] 
print("Enter the adjacency matrix:") 
for i in range(n): 
    row = list(map(int, input().split())) 
    for j in range(i, n): 
        if row[j]: 
            edges.append((i, j, row[j])) 
kruskals(n, edges)
"""
