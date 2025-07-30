def min_edit_distance(s1, s2, ic, dc, cc):
    n1, n2 = len(s1), len(s2)
    dp = [[0] * (n2 + 1) for _ in range(n1 + 1)]
   
    for i in range(n1 + 1):
        dp[i][0] = i * dc
    for j in range(n2 + 1):
        dp[0][j] = j * ic  
    for i in range(1, n1 + 1):
        for j in range(1, n2 + 1):
            cost = 0 if s1[i - 1] == s2[j - 1] else cc
            dp[i][j] = min(
                dp[i - 1][j] + dc,      
                dp[i][j - 1] + ic,      
                dp[i - 1][j - 1] + cost
            )
    print("The Cost Matrix is:")
    for row in dp:
        print(row)
   
    return dp[n1][n2]


s1 = input("Enter First String: ")
s2 = input("Enter Second String: ")
ic = int(input("Enter Insertion Cost: "))
dc = int(input("Enter Deletion Cost: "))
cc = int(input("Enter Substitution Cost: "))


cost = min_edit_distance(s1, s2, ic, dc, cc)
print("The Total Cost is:", cost)


code = '''
def min_edit_distance(s1, s2, ic, dc, cc):
    n1, n2 = len(s1), len(s2)
    dp = [[0] * (n2 + 1) for _ in range(n1 + 1)]
   
    for i in range(n1 + 1):
        dp[i][0] = i * dc
    for j in range(n2 + 1):
        dp[0][j] = j * ic  
    for i in range(1, n1 + 1):
        for j in range(1, n2 + 1):
            cost = 0 if s1[i - 1] == s2[j - 1] else cc
            dp[i][j] = min(
                dp[i - 1][j] + dc,      
                dp[i][j - 1] + ic,      
                dp[i - 1][j - 1] + cost
            )
    print("The Cost Matrix is:")
    for row in dp:
        print(row)
   
    return dp[n1][n2]


s1 = input("Enter First String: ")
s2 = input("Enter Second String: ")
ic = int(input("Enter Insertion Cost: "))
dc = int(input("Enter Deletion Cost: "))
cc = int(input("Enter Substitution Cost: "))


cost = min_edit_distance(s1, s2, ic, dc, cc)
print("The Total Cost is:", cost)

'''

def getCode():
    global code
    print(code)

    