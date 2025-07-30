code="""
def get_blank_pos(puzzle):
    for i in range(len(puzzle)):
        for j in range(len(puzzle)):
            if puzzle[i][j] == 0:
                return i, j

def actions_done(preState):
    nextState = []
    position = get_blank_pos(preState)
    i, j = position[0], position[1]

    # Move blank tile up
    if i > 0:
        new = [x[:] for x in preState]
        new[i][j], new[i-1][j] = new[i-1][j], new[i][j]
        nextState.append(new)

    # Move blank tile down
    if i < 2:
        new = [x[:] for x in preState]
        new[i][j], new[i+1][j] = new[i+1][j], new[i][j]
        nextState.append(new)

    # Move blank tile left
    if j > 0:
        new = [x[:] for x in preState]
        new[i][j], new[i][j-1] = new[i][j-1], new[i][j]
        nextState.append(new)

    # Move blank tile right
    if j < 2:
        new = [x[:] for x in preState]
        new[i][j], new[i][j+1] = new[i][j+1], new[i][j]
        nextState.append(new)

    return nextState

def bfs(initial, goal):
    que = [(initial, [])]
    visited = set()
    visited.add(tuple(map(tuple, initial)))

    while que:
        state, path = que.pop(0)
        if state == goal:
            return path

        for next in actions_done(state):
            next_tuple = tuple(map(tuple, next))
            if next_tuple not in visited:
                que.append((next, path + [next]))
                visited.add(next_tuple)

    return None

# Main program
initial_state = []
goal_state = []

print("Enter the initial state (3 rows of 3 numbers each, use 0 for blank):")
for i in range(3):
    initial_state.append(list(map(int, input().split())))

print("Initial state:")
print(initial_state)

print("Enter the goal state (3 rows of 3 numbers each):")
for i in range(3):
    goal_state.append(list(map(int, input().split())))

print("Goal state:")
print(goal_state)

path = bfs(initial_state, goal_state)
step = 1

if path:
    print("Solution found in", len(path), "steps:")
    for state in path:
        print("Step:", step)
        step += 1
        for row in state:
            print(row)
        print()
else:
    print("No path")
"""

def getCode():
    global code
    print(code)
    
 