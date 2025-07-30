code  = '''
def get_matrix(prompt):
    print(prompt)
    return [list(map(int, input().split())) for _ in range(3)]

def find_blank(state):
    for i, row in enumerate(state):
        if 0 in row:
            return i, row.index(0)

def generate_moves(state):
    x, y = find_blank(state)
    moves, directions = [], {'Up': (-1, 0), 'Down': (1, 0), 'Left': (0, -1), 'Right': (0, 1)}
    
    for move, (dx, dy) in directions.items():
        nx, ny = x + dx, y + dy
        if 0 <= nx < 3 and 0 <= ny < 3:
            new_state = [row[:] for row in state]
            new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
            moves.append((move, new_state))
    
    return moves[::-1]

def dfs(initial, goal):
    stack, visited = [(initial, [], 0)], {tuple(map(tuple, initial))}
    
    while stack:
        state, path, step = stack.pop()
        print(f"Step {step}: {path[-1] if path else 'Start'}\n" + "\n".join(" ".join(map(str, row)) for row in state) + "\n")
        
        if state == goal:
            print("Goal reached!")
            return
        
        for move, new_state in generate_moves(state):
            state_tuple = tuple(map(tuple, new_state))
            if state_tuple not in visited:
                visited.add(state_tuple)
                stack.append((new_state, path + [move], step + 1))

if __name__ == "__main__":
    initial, goal = get_matrix("Enter initial state (3x3, space as 0):"), get_matrix("Enter goal state (3x3, space as 0):")
    print("\nSolving 8-puzzle using DFS:\n")
    dfs(initial, goal)
'''

def getCode():
    global code
    print(code)
    