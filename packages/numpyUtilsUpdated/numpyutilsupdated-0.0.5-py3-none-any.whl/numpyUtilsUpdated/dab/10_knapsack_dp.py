code="""
def knapsack_dp(profit, W, n, weight): 
    dp = [[0] * (W + 1) for _ in range(n + 1)] 
    for i in range(1, n + 1): 
        for j in range(W + 1): 
            if weight[i - 1] > j: 
                dp[i][j] = dp[i - 1][j] 
            else: 
                dp[i][j] = max(profit[i - 1] + dp[i - 1][j - weight[i - 1]], dp[i - 1][j]) 
    for row in dp: 
        print(' '.join(map(str, row))) 
    items = [] 
    i, j = n, W 
    while i > 0 and j > 0: 
        if dp[i][j] != dp[i - 1][j]: 
            items.append((weight[i - 1], profit[i - 1])) 
            j -= weight[i - 1] 
        i -= 1 
    print("Included Weights & Profits:", ' '.join(f"({w}, {p})" for w, p in items)) 
    print(f"Maximum Profit: {dp[n][W]}") 

n = int(input("Enter size of n: ")) 
W = int(input("Enter knapsack capacity: ")) 
profit = list(map(int, input("Enter profits: ").split())) 
weight = list(map(int, input("Enter weights: ").split())) 
knapsack_dp(profit, W, n, weight)
"""
