def bellman_ford(matrix, source):
    vertices = len(matrix)
    edges = [(i, j, matrix[i][j]) for i in range(vertices) for j in range(vertices) if matrix[i][j] != x and i != j]
    dist = [x] * vertices
    dist[source] = 0


    for _ in range(vertices - 1):
        for u, v, w in edges:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w


    if any(dist[u] + w < dist[v] for u, v, w in edges):
        print("Graph contains a negative weight cycle!")
        return None


    return dist


x = float('inf')
matrix = [
    [0, -1, 4, x, x],
    [x, 0, 3, 2, 2],
    [x, x, 0, x, x],
    [x, 1, 5, 0, x],
    [x, x, x, -3, 0]
]
source = 0


distances = bellman_ford(matrix, source)
if distances:
    print("Shortest distances from source:", distances)


code = '''
def bellman_ford(matrix, source):
    vertices = len(matrix)
    edges = [(i, j, matrix[i][j]) for i in range(vertices) for j in range(vertices) if matrix[i][j] != x and i != j]
    dist = [x] * vertices
    dist[source] = 0


    for _ in range(vertices - 1):
        for u, v, w in edges:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w


    if any(dist[u] + w < dist[v] for u, v, w in edges):
        print("Graph contains a negative weight cycle!")
        return None


    return dist


x = float('inf')
matrix = [
    [0, -1, 4, x, x],
    [x, 0, 3, 2, 2],
    [x, x, 0, x, x],
    [x, 1, 5, 0, x],
    [x, x, x, -3, 0]
]
source = 0


distances = bellman_ford(matrix, source)
if distances:
    print("Shortest distances from source:", distances)

'''

def getCode():
    global code
    print(code)

    