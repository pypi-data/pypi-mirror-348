code = '''
def get_neighbors(state):
    i = state.index(0)
    moves = {'up': -3, 'down': 3, 'left': -1, 'right': 1}
    return [swap(state, i, i + d) for m, d in moves.items()
            if 0 <= i + d < 9 and abs((i + d) // 3 - i // 3) + abs((i + d) % 3 - i % 3) == 1]


def swap(state, i, j):
    s = state[:]
    s[i], s[j] = s[j], s[i]
    return s


def print_matrix(state):
    for i in range(0, 9, 3):
        print(' '.join(map(str, state[i:i+3])))
    print()


def dfs_8_puzzle(start, goal, depth_limit):
    stack, visited = [(start, [])], {tuple(start)}
    while stack:
        state, path = stack.pop()
        if state == goal:
            for i, s in enumerate(path):
                print(f"Step {i+1}:")
                print_matrix(s)
            return
        if len(path) < depth_limit:
            for n in get_neighbors(state)[::-1]:
                if tuple(n) not in visited:
                    visited.add(tuple(n))
                    stack.append((n, path + [n]))
    print("No solution found within depth limit.")


print("Enter 3 rows:")
start = [int(x) for _ in range(3) for x in input(f"Row {_+1}: ").split()]
depth_limit = int(input("Enter Depth limit: "))
goal = [1, 2, 3, 4, 5, 6, 7, 8, 0]
dfs_8_puzzle(start, goal, depth_limit)
'''

def getCode():
    global code
    print(code)
    