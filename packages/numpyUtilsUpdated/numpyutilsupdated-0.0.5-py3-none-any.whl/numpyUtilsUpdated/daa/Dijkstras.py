def dijkstra(graph, start):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    visited = []


    while len(visited) < len(graph):
        min_node = min((node for node in graph if node not in visited), key=lambda x: distances[x], default=None)
        if min_node is None:
            break
       
        visited.append(min_node)


        for neighbor, weight in graph[min_node].items():
            if neighbor not in visited:
                distances[neighbor] = min(distances[neighbor], distances[min_node] + weight)


    return distances




graph = {
    'A': {'B': 4, 'C': 2},
    'B': {'A': 4, 'C': 5, 'D': 10},
    'C': {'A': 2, 'B': 5, 'D': 3},
    'D': {'B': 10, 'C': 3}
}


start_node = 'B'
shortest_paths = dijkstra(graph, start_node)


print(f"\nShortest distances from {start_node}:")
for node, distance in shortest_paths.items():
    print(f"{node}: {distance}")


code = '''
def dijkstra(graph, start):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    visited = []


    while len(visited) < len(graph):
        min_node = min((node for node in graph if node not in visited), key=lambda x: distances[x], default=None)
        if min_node is None:
            break
       
        visited.append(min_node)


        for neighbor, weight in graph[min_node].items():
            if neighbor not in visited:
                distances[neighbor] = min(distances[neighbor], distances[min_node] + weight)


    return distances




graph = {
    'A': {'B': 4, 'C': 2},
    'B': {'A': 4, 'C': 5, 'D': 10},
    'C': {'A': 2, 'B': 5, 'D': 3},
    'D': {'B': 10, 'C': 3}
}


start_node = 'B'
shortest_paths = dijkstra(graph, start_node)


print(f"\nShortest distances from {start_node}:")
for node, distance in shortest_paths.items():
    print(f"{node}: {distance}")
'''

def getCode():
    global code
    print(code)
    