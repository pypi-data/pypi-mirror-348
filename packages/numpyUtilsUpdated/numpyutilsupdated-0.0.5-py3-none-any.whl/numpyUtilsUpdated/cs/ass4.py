code = '''
import numpy as np 
 
y = list(map(int, input("Enter Y-values: ").split())) 
n = int(input("ENter no. of samples: ")) + 1 
N = len(y) 
 
lists = [[] for _ in range(n)] 
 
lists[0] = [1]*N 
 
for i in range(1, n): 
    lists[i] = list(map(int, input(f"Enter values of Sample{i}: ").split())) 
    
x = np.transpose(lists) 
xt = lists 
xt_x = np.dot(xt, x) 
xt_x_I = np.linalg.inv(xt @ x) 
xt_y = np.dot(xt, y) 
beta = np.dot(xt_x_I, xt_y) 
 
output = f"{beta[0]:.2f}" 
 
for i in range(1, len(beta)): 
    if beta[i] >= 0: 
        output += f" + {beta[i]:.2f}x{i}" 
    else: 
        output += f" - {abs(beta[i]):.2f}x{i}" 
 
print(output) 

----------------------------------------------------------------------
Question_2

mport numpy as np 
 
y = [] 
for i in range(2): 
    y.append(list(map(int, input("Enter values of Y: ").split()))) 
n = int(input("Enter no. of smaples: ")) + 1 
 
lists = [[] for _ in range(n)] 
lists[0] = [1]*len(y[0]) 
 
for i in range(1, n-1): 
    lists[i] = list(map(int, input(f"Enter values of sample{i}: ").split())) 
lists[n-1] = list(map(float, input(f"Enter values of sample{i}: ").split())) 
 
x = np.transpose(lists) 
xt = lists 
xtx = np.dot(xt, x) 
xtx_I = np.linalg.inv(xtx) 
xty = np.dot(xt, np.transpose(y)) 
beta = np.transpose(np.dot(xtx_I, xty)) 
 
output_1 = f"Y1 : {beta[0][0]:.2f}" 
output_2 = f"Y2 : {beta[1][0]:.2f}" 
for i in range(1, len(beta[0])): 
    if beta[0][i] >= 0: 
        output_1 += f" + {beta[0][i]:.2f} x{i}" 
    else: 
        output_1 += f" - {-beta[0][i]:.2f} x{i}" 
for i in range(1, len(beta[1])): 
    if beta[1][i] >= 0: 
        output_2 += f" + {beta[1][i]:.2f} x{i}" 
    else: 
        output_2 += f" - {-beta[1][i]:.2f} x{i}" 
print(output_1) 
print(output_2) 

'''

def getCode():
    global code
    print(code)

