import sys

# MAX = 10

def tsp(n, dist, visited, current):
    if visited == (1 << n) - 1:
        return dist[current][0]
    
    min_cost = sys.maxsize 
    for i in range(n):
        if (visited & (1 << i)) == 0:  
            cost = dist[current][i] + tsp(n, dist, visited | (1 << i), i)
            min_cost = min(min_cost, cost)
    
    return min_cost

def main():
    n = int(input("Enter number of nodes: "))
    dist = []
    print("Enter the adjacency matrix:")
    for i in range(n):
        row = list(map(int, input().split()))
        dist.append(row)
    
    visited = 1  # Starting at city 0
    start_city = 0
    min_cost = tsp(n, dist, visited, start_city)
    print(f"Minimum cost: {min_cost}")

if __name__ == "__main__":
    main()
