code = '''
import random

grid_size = 4


def generate_world():
    world = [[' ' for _ in range(grid_size)] for _ in range(grid_size)]
   
    # Place Wumpus, Gold, and Pits randomly
    elements = ['W', 'G', 'P', 'P']
    positions = random.sample([(i, j) for i in range(grid_size) for j in range(grid_size) if (i, j) != (0, 0)], len(elements))
   
    for (x, y), elem in zip(positions, elements):
        world[x][y] = elem
   
    return world


def display_percepts(world, x, y):
    percepts = []
   
    if any(world[i][j] == 'W' for i, j in get_neighbors(x, y)):
        percepts.append("Stench detected!")
    if any(world[i][j] == 'P' for i, j in get_neighbors(x, y)):
        percepts.append("Breeze detected!")
   
    return percepts


def get_neighbors(x, y):
    neighbors = []
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < grid_size and 0 <= ny < grid_size:
            neighbors.append((nx, ny))
    return neighbors


def display_state(x, y):
    for i in range(grid_size):
        for j in range(grid_size):
            if (i, j) == (x, y):
                print('A', end=' ')
            else:
                print('.', end=' ')
        print()
    print()


if __name__ == "__main__":
    world = generate_world()
    x, y = 0, 0  # Starting position
   
    while True:
        display_state(x, y)
        percepts = display_percepts(world, x, y)
        for p in percepts:
            print(p)
       
        move = input("Move (up/down/left/right): ").strip().lower()
        if move == "up" and x > 0:
            x -= 1
        elif move == "down" and x < grid_size - 1:
            x += 1
        elif move == "left" and y > 0:
            y -= 1
        elif move == "right" and y < grid_size - 1:
            y += 1
        else:
            print("Invalid move. Try again.")
            continue
       
        if world[x][y] == 'W':
            print("You were eaten by the Wumpus! Game Over.")
            break
        elif world[x][y] == 'P':
            print("You fell into a pit! Game Over.")
            break
        elif world[x][y] == 'G':
            print("You found the Gold! You Win!")
            break
            
'''

def getCode():
    global code
    print(code)
