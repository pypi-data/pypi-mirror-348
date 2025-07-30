code = '''

def min_edit_distance(s1, s2, ic, dc, cc):
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(m + 1): dp[i][0] = i * dc
    for j in range(n + 1): dp[0][j] = j * ic
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            cost = 0 if s1[i - 1] == s2[j - 1] else cc
            dp[i][j] = min(dp[i - 1][j] + dc, dp[i][j - 1] + ic, dp[i - 1][j - 1] + cost)
            
    print("The Cost Matrix is:")
    for row in dp: print(" ".join(map(str, row)))
    return dp[m][n]

s1 = input("Enter First String: ")
s2 = input("Enter Second String: ")
ic = int(input("Enter Insertion Cost: "))
dc = int(input("Enter Deletion Cost: "))
cc = int(input("Enter Substitution Cost: "))

print("The Total Cost is:", min_edit_distance(s1, s2, ic, dc, cc))

'''