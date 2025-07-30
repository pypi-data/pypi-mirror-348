code = """
def waterJug(target, ljug, sjug):
    jug1 = jug2 = 0
    steps = 0

    while jug1 != target and jug2 != target:
        if jug2 == 0:
            jug2 = sjug  # Fill small jug
        elif jug1 + jug2 <= ljug:
            jug1 += jug2  # Pour small into large
            jug2 = 0
        else:
            transfer = ljug - jug1
            jug2 -= transfer
            jug1 = ljug  # Fill large to its capacity
        steps += 1
        print(f"Step {steps}: Jug1 = {jug1}L, Jug2 = {jug2}L")

        if jug1 == target or jug2 == target:
            break

        if jug1 == ljug:
            jug1 = 0  # Empty large jug
            steps += 1
            print(f"Step {steps}: Jug1 = {jug1}L, Jug2 = {jug2}L")

    print(f"\nTarget of {target}L reached!")
    print("Total steps:", steps)


# Inputs
target = int(input("Enter target amount: "))
ljug = int(input("Enter large jug capacity: "))
sjug = int(input("Enter small jug capacity: "))

print("\nSteps:")
waterJug(target, ljug, sjug)
"""

def getCode():
    global code
    print(code)
    
 