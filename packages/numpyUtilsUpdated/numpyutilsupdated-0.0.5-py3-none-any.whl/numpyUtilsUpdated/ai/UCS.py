code = '''
def get_matrix(): return [list(map(int, input().split())) for _ in range(3)]

def find_blank(state): return next((i, j) for i in range(3) for j in range(3) if not state[i][j])

def swap(state, x1, y1, x2, y2):
    new_state = [row[:] for row in state]
    new_state[x1][y1], new_state[x2][y2] = new_state[x2][y2], new_state[x1][y1]
    return new_state

def print_state(state): print("\n".join(" ".join(map(str, row)) for row in state), "\n")

def uniform_cost_search(initial, goal):
    queue, visited = [(0, initial, [])], set()
    while queue:
        queue.sort()
        cost, state, path = queue.pop(0)
        if state == goal: [print_state(step) for step in path + [state]]; return
        state_tuple = tuple(map(tuple, state))
        if state_tuple in visited: continue
        visited.add(state_tuple)
        x, y = find_blank(state)
        for nx, ny in [(x-1,y), (x+1,y), (x,y-1), (x,y+1)]:
            if 0 <= nx < 3 and 0 <= ny < 3:
                queue.append((cost+1, swap(state, x, y, nx, ny), path + [state]))

print("Enter initial state:")
initial_state = get_matrix()
print("Enter goal state:")
goal_state = get_matrix()
print("Solution Steps:")
uniform_cost_search(initial_state, goal_state)

'''
def getCode():
    global code
    print(code)
    