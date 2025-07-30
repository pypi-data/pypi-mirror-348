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

def dls(state, goal, depth_limit):
    if state == goal:
        return [state]
    if depth_limit == 0:
        return None
    for next_state in actions_done(state):
        path = dls(next_state, goal, depth_limit - 1)
        if path is not None:
            return [state] + path
    return None

def ids(initial, goal, max_depth):
    for depth_limit in range(max_depth + 1):
        path = dls(initial, goal, depth_limit)
        if path is not None:
            return path
    return None

# Main program
initial_state = []
goal_state = []

print("Enter the initial state (3 rows of 3 numbers each, use 0 for blank):")
for i in range(3):
    initial_state.append(list(map(int, input().split())))

print("Initial state:")
for row in initial_state:
    print(row)

print("Enter the goal state (3 rows of 3 numbers each):")
for i in range(3):
    goal_state.append(list(map(int, input().split())))

print("Goal state:")
for row in goal_state:
    print(row)

max_depth = 10
path = ids(initial_state, goal_state, max_depth)
step = 0

if path:
    print("Solution found in", len(path) - 1, "steps:")
    for state in path:
        print("Step:", step)
        step += 1
        for row in state:
            print(row)
        print()
else:
    print("No path found within the depth limit")
"""

def getCode():
    global code
    print(code)
    
 