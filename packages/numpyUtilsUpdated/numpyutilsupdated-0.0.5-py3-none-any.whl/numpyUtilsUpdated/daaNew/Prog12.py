code = '''

def tsp(n, dist, visited, current):
    if all(visited):  
        return dist[current][0]
    
    min_cost = float('inf')
    for i in range(n):
        if not visited[i]:
            visited[i] = True
            cost = dist[current][i] + tsp(n, dist, visited, i)
            min_cost = min(min_cost, cost)
            visited[i] = False
    
    return min_cost

if __name__ == "__main__":
    n = 4
    # dist = [
    #     [0, 10, 15, 20],
    #     [10, 0, 35, 25],
    #     [15, 35, 0, 30],
    #     [20, 25, 30, 0]
    # ]
    
    dist = [
        [0 ,10 ,15 ,20],
        [5 ,0 ,9 ,10],
        [6 ,13 ,0 ,12],
        [8 ,8 ,9 ,0]
    ]
    print("\n".join(map(str, dist)))
    visited = [False] * n
    visited[0] = True 
    
    min_cost = tsp(n, dist, visited, 0)
    print(f"Minimum cost: {min_cost}")

'''