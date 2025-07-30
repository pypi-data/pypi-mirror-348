code="""
d = {
    'a': [['z', 374], ['t', 329], ['s', 253]],
    'z': [['a', 366], ['o', 380]],
    'o': [['z', 374], ['s', 253]],
    's': [['a', 366], ['f', 176], ['r', 193]],
    't': [['a', 366], ['l', 244]],
    'l': [['t', 329], ['m', 241]],
    'm': [['l', 244], ['d', 242]],
    'd': [['c', 160], ['m', 241]],
    'c': [['d', 242], ['r', 193], ['p', 100]],
    'r': [['s', 253], ['c', 160], ['p', 100]],
    'p': [['r', 193], ['b', 0], ['c', 160]],
    'f': [['s', 253], ['b', 0]]
}

def Shortest_path(sv, dv):
    if sv == dv:
        return
    minn = 1000
    for i in d[sv]:
        if i[1] < minn:
            minn = i[1]
            sv = i[0]
    print(sv, end=' ')
    Shortest_path(sv, dv)

a = input("Enter the Source Vertex: ")
b = input("Enter the Destination Vertex: ")
print("The Shortest Path is:", a, end=' ')
Shortest_path(a, b)
"""

def getCode():
    global code
    print(code)
    
 