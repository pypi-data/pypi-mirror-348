code = '''
def show(b):
    for r in b:
        print(" | ".join(r))
    print("- " * 9)

def win(b, p):
    for i in range(3):
        if all(b[i][j]==p for j in range(3)): return True
        if all(b[j][i]==p for j in range(3)): return True
    if all(b[i][i]==p for i in range(3)): return True
    if all(b[i][2-i]==p for i in range(3)): return True
    return False

def full(b):
    return all(c != " " for r in b for c in r)

def minimax(b, turn):
    if win(b, "X"): return 1
    if win(b, "O"): return -1
    if full(b): return 0
    best = -2 if turn else 2
    p = "X" if turn else "O"
    for i in range(3):
        for j in range(3):
            if b[i][j] == " ":
                b[i][j] = p
                score = minimax(b, not turn)
                b[i][j] = " "
                if turn: best = max(best, score)
                else: best = min(best, score)
    return best

def best_move(b):
    best, pos = -2, None
    for i in range(3):
        for j in range(3):
            if b[i][j] == " ":
                b[i][j] = "X"
                score = minimax(b, False)
                b[i][j] = " "
                if score > best:
                    best = score
                    pos = (i, j)
    return pos

b = [[" "] * 3 for _ in range(3)]
print("Tic-Tac-Toe (O=You, X=AI)")
show(b)

while True:
    r, c = map(int, input("Row Col: ").split())
    if b[r][c] != " ":
        print("Invalid"); continue
    b[r][c] = "O"
    show(b)
    if win(b, "O"): print("You win!"); break
    if full(b): print("Tie!"); break
    m = best_move(b)
    if m: b[m[0]][m[1]] = "X"
    print("AI move:")
    show(b)
    if win(b, "X"): print("AI wins!"); break
    if full(b): print("Tie!"); break

'''

def getCode():
    global code
    print(code)
    