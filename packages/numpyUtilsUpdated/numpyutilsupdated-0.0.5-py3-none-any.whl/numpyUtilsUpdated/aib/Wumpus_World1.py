code="""
import random

size = 4
visited = [[0, 0]]
grid = [['-' for _ in range(size)] for _ in range(size)]
agent_position = (0, 0)

def generate_world():
    # Place the wumpus
    wumpus_pos = get_random_position()
    grid[wumpus_pos[0]][wumpus_pos[1]] = 'W'
    
    # Place the gold
    gold_pos = get_random_position()
    grid[gold_pos[0]][gold_pos[1]] = 'G'
    
    # Place the pits
    num_pits = size // 2
    for _ in range(num_pits):
        pit_pos = get_random_position()
        grid[pit_pos[0]][pit_pos[1]] = 'P'

def get_random_position():
    while True:
        x = random.randint(0, size-1)
        y = random.randint(0, size-1)
        if [x, y] not in visited:
            visited.append([x, y])
            return x, y

def move_agent(direction):
    global agent_position
    x, y = agent_position
    if direction == 'up' and x > 0:
        agent_position = (x - 1, y)
    elif direction == 'down' and x < size - 1:
        agent_position = (x + 1, y)
    elif direction == 'left' and y > 0:
        agent_position = (x, y - 1)
    elif direction == 'right' and y < size - 1:
        agent_position = (x, y + 1)

def is_game_over():
    x, y = agent_position
    if grid[x][y] == 'W':
        return "You were eaten by the Wumpus! Game over."
    elif grid[x][y] == 'P':
        return "You fell into a pit! Game over."
    elif grid[x][y] == 'G':
        return "Congratulations! You found the gold and won the game."
    else:
        return False

def print_grid():
    for row in grid:
        print(" ".join(row))

generate_world()
print("Actions: up, down, left, right, quit")

while True:
    grid[agent_position[0]][agent_position[1]] = 'A'
    print_grid()
    grid[agent_position[0]][agent_position[1]] = '-'
    
    print(f"Current position: {agent_position}")
    action = input("Enter your action: ")
    
    if action == 'quit':
        break
    
    move_agent(action)
    result = is_game_over()
    
    if result:
        print(result)
        break
    else:
        print("Keep exploring!")
"""

def getCode():
    global code
    print(code)
    
 