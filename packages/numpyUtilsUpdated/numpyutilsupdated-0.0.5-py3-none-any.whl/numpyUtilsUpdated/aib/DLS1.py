code="""
def get_blank_pos(puzzle):
    for i in range(3):
        for j in range(3):
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
    return dls_recursive(state, goal, depth_limit, 0, [state])

def dls_recursive(state, goal, depth_limit, depth, path):
    if state == goal:
        return path
    if depth >= depth_limit:
        return None
    
    for next_state in actions_done(state):
        new_path = path + [next_state]
        result = dls_recursive(next_state, goal, depth_limit, depth + 1, new_path)
        if result:
            return result
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

depth_limit = int(input("Enter the depth limit: "))
path = dls(initial_state, goal_state, depth_limit)

if path:
    print("Solution found within depth limit:")
    for step, state in enumerate(path):
        print("Step:", step + 1)
        for row in state:
            print(row)
        print()
else:
    print("No solution found within depth limit")
"""

def getCode():
    global code
    print(code)
    
 