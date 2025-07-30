code = '''

def initialize_environment():
    n_rooms = int(input("No.of rooms: "))
    room_dic = {}
    for i in range(1, n_rooms + 1):
        r_num = f"Room{i}"
        status = input(f"Enter status of {r_num} (Clean/Dirty): ").strip().capitalize()
        room_dic[r_num] = status
    return room_dic


def sense(room_dic, cur_loc):
    return room_dic[cur_loc]


def suck(room_dic, cur_loc):
    if room_dic[cur_loc] == "Dirty":
        print(f"Cleaning {cur_loc}")
        room_dic[cur_loc] = "Clean"


def isdone(room_dic):
    return all(status == "Clean" for status in room_dic.values())


def move(room_dic, cur_loc):
    room_index = list(room_dic)
    cur_index = room_index.index(cur_loc)
    next_loc = room_index[(cur_index + 1) % len(room_index)]
    print(f"Moving from {cur_loc} to {next_loc}")
    return next_loc


def act(room_dic, cur_loc):
    if sense(room_dic, cur_loc) == "Dirty":
        suck(room_dic, cur_loc)
        return cur_loc
    else:
        return move(room_dic, cur_loc)

if __name__ == "__main__":
    room_dic = initialize_environment()
    cur_loc = list(room_dic.keys())[0]
    step = 1
    print("\nInitial State:", room_dic)
    while not all(status == "Clean" for status in room_dic.values()):
        print(f"\nStep {step}:")
        print(f"Current Location: {cur_loc}")
        cur_loc = act(room_dic, cur_loc)
        print("Environment State:", room_dic)
        step += 1
    print("\nFINAL STATE:", room_dic,"\n")

'''

def getCode():
    global code
    print(code)
