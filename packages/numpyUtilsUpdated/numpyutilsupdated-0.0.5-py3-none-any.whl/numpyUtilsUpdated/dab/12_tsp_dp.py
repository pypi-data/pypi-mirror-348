code="""
def tsp(dist): 
    n = len(dist) 
    dp = {} 
    def solve(mask, pos): 
        if mask == (1 << n) - 1: 
            return dist[pos][0] 
        if (mask, pos) in dp: 
            return dp[(mask, pos)] 
        ans = float('inf') 
        for city in range(n): 
            if (mask & (1 << city)) == 0: 
                new_mask = mask | (1 << city) 
                ans = min(ans, dist[pos][city] + solve(new_mask, city)) 
        dp[(mask, pos)] = ans 
        return ans 
    return solve(1, 0) 

n = int(input("Enter number of nodes: ")) 
dist = [] 
print("Enter the adjacency matrix:") 
for _ in range(n): 
    dist.append(list(map(int, input().split()))) 
print(f"Minimum cost: {tsp(dist)}")
"""