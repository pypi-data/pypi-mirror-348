code = '''
import numpy as np
import matplotlib.pyplot as plt


x = list(map(int, input("Enter x coordinates : ").split()))
y = list(map(float, input("Enter y coordinates : ").split()))


if len(x) != len(y):
    exit(0)


xy_list = []
for i in range(0, len(x)):
    xy_list.append(x[i] * y[i])


x2_list = [i ** 2 for i in x]


A = np.array([
    [len(x), sum(x)],
    [sum(x), sum(x2_list)]
    ])
B = np.array([sum(y), sum(xy_list)])


a, b = np.linalg.solve(A,B)


print(f"Line of best fit: y = {a:.2f}x + {b:.2f}")


plt.scatter(x, y)


plt.show()

Output :
PS Z:\Y23CM012\work_CS_lab> python .\lab_1\best_fit_st_line.py 
Enter x coordinates : 1 2 3 4 6 8
Enter y coordinates : 2.4 3 3.6 4 5 6
Line of best fit: y = 1.98x + 0.51

------------------------------------------------------------------------------

import numpy as np
import matplotlib.pyplot as plt


x = list(map(int, input("Enter x coordinates : ").split()))
y = list(map(float, input("Enter  y coordinates : ").split()))


if len(x) != len(y):
    exit(0)


xy_list = []
x2y_list = []
for i in range(0, len(x)):
    xy_list.append(x[i] * y[i])
    x2y_list.append((x[i] ** 2) * y[i])


x2_list = [i ** 2 for i in x]
x3_list = [i ** 3 for i in x]
x4_list = [i ** 4 for i in x]


A = np.array([
    [len(x), sum(x), sum(x2_list)],
    [sum(x), sum(x2_list), sum(x3_list)],
    [sum(x2_list), sum(x3_list), sum(x4_list)],
    ])
B = np.array([sum(y), sum(xy_list), sum(x2y_list)])


a, b, c = np.linalg.solve(A,B)


print(f"Line of best fit: y = {a:.2f}  {b:.2f}x  {c:.2f}x^2")


plt.scatter(x, y)


plt.show()

Output : 
PS Z:\Y23CM012\work_CS_lab> python .\lab_1\best_fit_parabola.py
Enter x coordinates : 0 1 2 3 4
Enter  y coordinates : 1 1.8 1.3 2.5 6.3
Line of best fit: y = 1.42  -1.07x  0.55x^2

'''

def getCode():
    global code
    print(code)
    