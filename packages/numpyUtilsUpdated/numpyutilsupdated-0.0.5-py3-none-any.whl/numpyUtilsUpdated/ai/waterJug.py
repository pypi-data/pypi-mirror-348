code = '''

def printf(step, jug1, jug2):
    print(f"Step-{step}: Large Jug = {jug1}, Small Jug = {jug2}")


def WaterJug(goal, ljug, sjug):
    jug1 = jug2 = 0  
    step = 0
    print("Initial state")
    printf(step, jug1, jug2)


    while jug1 != goal and jug2 != goal:
        if jug1 == 0:
            jug1 = ljug
            step += 1
            printf(step, jug1, jug2)


        if jug1 > 0:
            transfer = min(jug1, sjug - jug2)
            jug1 -= transfer
            jug2 += transfer
            step += 1
            printf(step, jug1, jug2)


        if jug1 == goal or jug2 == goal:
            break


        if jug2 == sjug:
            jug2 = 0
            step += 1
            printf(step, jug1, jug2)


    print(f"No. of steps: {step}")
    print("Reached Goal State.")


ljug = int(input("Enter capacity of large jug: "))
sjug = int(input("Enter capacity of small jug: "))
goal = int(input("Enter goal capacity: "))


if goal > max(ljug, sjug):
    print("Goal cannot be greater than the largest jug capacity!")
elif goal % (gcd := __import__('math').gcd(ljug, sjug)) != 0:
    print(f"Goal must be a multiple of GCD({ljug}, {sjug}) = {gcd}")
else:
    WaterJug(goal, ljug, sjug)

'''

def getCode():
    global code
    print(code)