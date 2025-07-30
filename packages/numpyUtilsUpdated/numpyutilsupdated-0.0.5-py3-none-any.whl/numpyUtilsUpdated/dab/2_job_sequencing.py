code="""
def job_sequencing(n, profits, dead): 
    jobs = sorted(zip(profits, dead), key=lambda x: x[0], reverse=True) 
    max_dead = max(dead) 
    slots = [0] * max_dead 
    profit = 0 
    for p, d in jobs: 
        for j in range(d - 1, -1, -1): 
            if slots[j] == 0: 
                slots[j] = 1 
                profit += p 
                break 
    return profit 

n = int(input("Enter n: ")) 
profits = list(map(int, input("Enter profits: ").split())) 
dead = list(map(int, input("Enter deadlines: ").split())) 
print(f"Total profit: {job_sequencing(n, profits, dead)}")
"""
