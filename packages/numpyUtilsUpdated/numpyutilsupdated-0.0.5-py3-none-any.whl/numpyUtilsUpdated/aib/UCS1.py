code="""
from queue import PriorityQueue

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

def calculate_cost(path):
    return len(path)

def ucs(initial, goal):
    queue = PriorityQueue()
    queue.put((0, [initial]))  # (cost, path)
    visited = set()

    while not queue.empty():
        cost, path = queue.get()
        state = path[-1]

        if tuple(map(tuple, state)) in visited:
            continue

        visited.add(tuple(map(tuple, state)))

        if state == goal:
            return path

        for next_state in actions_done(state):
            if tuple(map(tuple, next_state)) not in visited:
                new_path = list(path)
                new_path.append(next_state)
                queue.put((calculate_cost(new_path), new_path))

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

path = ucs(initial_state, goal_state)
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
    print("No path")

"""

def getCode():
    global code
    print(code)
    
 