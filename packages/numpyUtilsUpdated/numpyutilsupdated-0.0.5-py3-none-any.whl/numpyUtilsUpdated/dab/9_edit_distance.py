code="""
def string_edit(s1, s2, ic, dc, cc): 
    n1, n2 = len(s1), len(s2) 
    dp = [[0] * (n2 + 1) for _ in range(n1 + 1)] 
    for i in range(n1 + 1): 
        dp[i][0] = i 
    for j in range(n2 + 1): 
        dp[0][j] = j 
    for i in range(1, n1 + 1): 
        for j in range(1, n2 + 1): 
            cost = 0 if s1[i - 1] == s2[j - 1] else cc 
            dp[i][j] = min(dp[i - 1][j] + dc, dp[i][j - 1] + ic, dp[i - 1][j - 1] + cost) 
    print("Cost Matrix:") 
    for row in dp: 
        print(' '.join(map(str, row))) 
    print(f"Total Cost: {dp[n1][n2]}") 

s1 = input("Enter First String: ") 
s2 = input("Enter Second String: ") 
ic, dc, cc = map(int, input("Enter Insertion, Deletion and Change Cost: ").split()) 
string_edit(s1, s2, ic, dc, cc)
"""