def Prim(graph):
    n = len(graph)
    selected = [False] * n
    mst = []
    sum = 0
    
    selected[0] = True
    
    for _ in range(n-1):
        min_weight = float('inf')
        u, v = -1, -1
        
        for i in range(n):
            if selected[i]:
                for j in range(n):
                    if not selected[j] and graph[i][j] > 0 and graph[i][j] < min_weight:
                        min_weight = graph[i][j]
                        u, v = i, j
        
        if u != -1 and v != -1:
            mst.append([u + 1, v + 1, min_weight])
            selected[v] = True
        
        sum += min_weight
    
    print("Initial , Next, Weight")    
    for ed in mst:
        print(ed)
    print(f"Total weight from 1st node yto cover all nodes: {sum}")
                


if __name__ == '__main__':
    graph = [
        [0, 2, 0, 6, 0],
        [2, 0, 3, 8, 5],
        [0, 3, 0, 0, 7],
        [6, 8, 0, 0, 9],
        [0, 5, 7, 9, 0]
    ]
    
    Prim(graph)

code = '''
def Prim(graph):
    n = len(graph)
    selected = [False] * n
    mst = []
    sum = 0
    
    selected[0] = True
    
    for _ in range(n-1):
        min_weight = float('inf')
        u, v = -1, -1
        
        for i in range(n):
            if selected[i]:
                for j in range(n):
                    if not selected[j] and graph[i][j] > 0 and graph[i][j] < min_weight:
                        min_weight = graph[i][j]
                        u, v = i, j
        
        if u != -1 and v != -1:
            mst.append([u + 1, v + 1, min_weight])
            selected[v] = True
        
        sum += min_weight
    
    print("Initial , Next, Weight")    
    for ed in mst:
        print(ed)
    print(f"Total weight from 1st node yto cover all nodes: {sum}")
                


if __name__ == '__main__':
    graph = [
        [0, 2, 0, 6, 0],
        [2, 0, 3, 8, 5],
        [0, 3, 0, 0, 7],
        [6, 8, 0, 0, 9],
        [0, 5, 7, 9, 0]
    ]
    
    Prim(graph)

'''
def getCode():
    global code
    print(code)
    