code = '''
graph = {'A': {'B': 6, 'F': 3}, 'B': {'C': 3, 'D': 2}, 'C': {'E': 5}, 'D': {'E': 8},
         'E': {'J': 5, 'I': 5}, 'F': {'G': 1, 'H': 7}, 'G': {'I': 3}, 'H': {'I': 2},
         'I': {'J': 3}, 'J': {}}
heuristic = {'A': 10, 'B': 8, 'C': 5, 'D': 7, 'E': 3, 'F': 6, 'G': 5, 'H': 3, 'I': 1, 'J': 0}


def gbfs(start, dest):
    open_list, closed = [start], []
    while open_list:
        cur = min(open_list, key=heuristic.get)
        open_list.remove(cur)
        closed.append(cur)
        if cur == dest:
            return closed
        open_list.extend(adj for adj in graph[cur] if adj not in open_list + closed)
    return None


start, end = input("Enter Starting Point: "), input("Enter Destination: ")
path = gbfs(start, end)
if path:
    for n in path:
        print(' '.join(f'[{n}, {heuristic[n]}]' ))
else:
    print("None")

'''

def getCode():
    global code
    print(code)
    