code="""
def greedy_knapsack(n, m, p, w): 
    ratios = sorted(zip(p, w), key=lambda x: x[0] / x[1], reverse=True) 
    profit = 0 
    for pi, wi in ratios: 
        if m >= wi: 
            profit += pi 
            m -= wi 
        else: 
            profit += pi * (m / wi) 
            break 
    return profit 

n = int(input("Enter size: ")) 
m = int(input("Enter capacity: ")) 
p = list(map(int, input("Enter profits: ").split())) 
w = list(map(int, input("Enter weights: ").split())) 
print(f"Total profit: {greedy_knapsack(n, m, p, w):.2f}")
"""
