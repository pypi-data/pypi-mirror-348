code = '''
n = 7
m = 3
variables = ["A", "B", "C", "D", "E", "F", "G"]

graph = [
    [0, 1, 1, 0, 0, 0, 0],
    [1, 0, 1, 1, 0, 0, 0],
    [1, 1, 0, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 0, 0],
    [0, 0, 1, 1, 0, 1, 0],
    [0, 0, 1, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0]
]
colors = ["R", "Y", "P"]
color = [0]*n

def is_Safe(curr, color, c):
    return all(graph[curr][i] == 0 or color[i] != c for i in range(n))

def graphColor(curr, color):
    if curr == n:
        return True
    for c in range(1, m+1):
        if is_Safe(curr, color, c):
            color[curr] = c
            if graphColor(curr + 1, color):
                return True
            color[curr] = 0
    return False

if graphColor(0, color):
    for i in range(n):
        print(f"{variables[i]}: {colors[color[i] - 1]}")
else:
    print("Solution does not exist")

'''

def getCode():
    global code
    print(code)