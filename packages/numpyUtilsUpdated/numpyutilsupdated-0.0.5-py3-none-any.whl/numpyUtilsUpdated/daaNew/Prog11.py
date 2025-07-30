code = '''

n = int(input("Enter size of n: "))
cap = int(input("Enter knapsack capacity: "))
profits = list(map(int, input("Enter profits: ").split()))
weights = list(map(int, input("Enter weights: ").split()))

dp = [[0] * (cap + 1) for _ in range(n + 1)]

for i in range(1, n + 1):
    for w in range(1, cap + 1):
        if weights[i - 1] <= w:
            dp[i][w] = max(profits[i - 1] + dp[i - 1][w - weights[i - 1]], dp[i - 1][w])
        else:
            dp[i][w] = dp[i - 1][w]

for row in dp:
    print(" ".join(map(str, row)))

w, items = cap, []
for i in range(n, 0, -1):
    if dp[i][w] != dp[i - 1][w]:
        items.append((weights[i - 1], profits[i - 1]))
        w -= weights[i - 1]

print("Included Weights & Profits:", " ".join(f"({w}, {p})" for w, p in reversed(items)))
print("Maximum Profit:", dp[n][cap])

'''