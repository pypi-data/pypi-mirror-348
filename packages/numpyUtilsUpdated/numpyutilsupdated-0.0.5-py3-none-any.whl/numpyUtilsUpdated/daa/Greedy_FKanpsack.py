profit = list(map(int,input("Enter Profits of items:").split()))
weight = list(map(int,input("Enter Weights of items:").split()))

if len(profit) != len(weight):
    print("Invalid Data...")
    exit(0)

u = int(input("Enter capacity of bag: "))
n = len(profit)
x = [0]*n
sum = 0

p_w = [p/w for p,w in zip(profit,weight)]
sol = sorted(zip(p_w,profit,weight),reverse=True)
sp_w, sprofit, sweight = zip(*sol)

for i in range(n):
    if sweight[i] <= u:  
        x[i] = 1 
        u -= sweight[i]  
    else:
        x[i] = round(u / sweight[i], 2)
        u = 0  
        break
    
print(f"Solution List: {x}")

for i,j in zip(x,sprofit):
    sum += i*j

print(f"Maximum profit is:{sum:.2f}")

code = '''
profit = list(map(int,input("Enter Profits of items:").split()))
weight = list(map(int,input("Enter Weights of items:").split()))

if len(profit) != len(weight):
    print("Invalid Data...")
    exit(0)

u = int(input("Enter capacity of bag: "))
n = len(profit)
x = [0]*n
sum = 0

p_w = [p/w for p,w in zip(profit,weight)]
sol = sorted(zip(p_w,profit,weight),reverse=True)
sp_w, sprofit, sweight = zip(*sol)

for i in range(n):
    if sweight[i] <= u:  
        x[i] = 1 
        u -= sweight[i]  
    else:
        x[i] = round(u / sweight[i], 2)
        u = 0  
        break
    
print(f"Solution List: {x}")

for i,j in zip(x,sprofit):
    sum += i*j

print(f"Maximum profit is:{sum:.2f}")
'''

def getCode():
    global code
    print(code)

    