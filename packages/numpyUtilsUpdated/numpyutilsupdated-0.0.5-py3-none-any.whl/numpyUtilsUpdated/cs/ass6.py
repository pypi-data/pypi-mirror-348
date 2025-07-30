code = '''
import numpy as np

n = int(input("Enter no. of variables: "))
x = [list(map(int, input().split())) for _ in range(n)]
x = np.transpose(x)

A = x - np.mean(x, axis = 0)
Varcov = np.dot(np.transpose(A), A) / len(A)

eval, evec = np.linalg.eigh(Varcov)
idx = np.argsort(eval)[::-1]
eval = eval[idx]
evec = evec[:, idx]

k = int(input("Enter threshold value: "))
cum_var = np.cumsum(eval) / np.sum(eval) * 100
stoppoint = np.sum(cum_var <= k) + 1

eval = eval[:stoppoint]
evec = evec[:, :stoppoint]
print(f'Retained Eigen Values :\n{eval}\n')
print(f'Retained Eigen Vectors:\n{evec}\n')

PCA = np.dot(x, evec)
print("PCA Matrix: \n",PCA)


--------------------------------------------

import numpy as np

n = int(input("ENter no. of variables: "))
x = [list(map(int, input().split())) for _ in range(n)]
x = np.transpose(x)

mu = np.mean(x, axis =0)
si = np.std(x, axis = 0, ddof = 1)

A = (x - mu) /si

Varcov = np.dot(np.transpose(A), A) / len(x)
print("VARCOVAR Matrix: \n", Varcov)

eval, evec = np.linalg.eigh(Varcov)
idx = np.argsort(eval)[::-1]
eval = eval[idx]
evec = evec[:, idx]

k = int(input("Enter Threshold Value: "))
cum_var = np.cumsum(eval) / sum(eval) *100
stoppoint = sum(cum_var <= k) + 1

eval = eval[:stoppoint]
evec = evec[:, :stoppoint]

f = np.transpose(evec * np.sqrt(eval))

h = np.sum(f**2, axis=0)
sumh = np.sum(h)
print(h)
print()
print(sumh)

pve = (eval/ np.sum(eval)) * 100
print(pve)

'''

def getCode():
    global code
    print(code)
    