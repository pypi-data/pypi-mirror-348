def knapsack(weights, values, capacity):
    n = len(values)

    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            if weights[i - 1] <= w:
                dp[i][w] = max(values[i - 1] + dp[i - 1][w - weights[i - 1]], dp[i - 1][w])
            else:
                dp[i][w] = dp[i - 1][w]

    w = capacity
    sel_wei = []
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            sel_wei.append(weights[i - 1])
            w -= weights[i - 1]

    sel_wei.reverse() 

    return dp[n][capacity], sel_wei, dp
# Example usage:
weights = list(map(int, input("Enter Weights: ").split()))
values = list(map(int, input("Enter Profits: ").split()))
capacity = int(input("Enter Capacity: "))

max_value, sel_wei, dps = knapsack(weights, values, capacity)
for row in dps:
    print(" ".join(map(str,row)))
print("Maximum value that can be obtained:", max_value)
print("Weights taken:", sel_wei)
