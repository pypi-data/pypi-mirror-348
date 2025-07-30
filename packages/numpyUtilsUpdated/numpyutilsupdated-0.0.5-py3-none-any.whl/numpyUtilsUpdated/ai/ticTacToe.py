code = '''

def print_board(b):
    for r in b:
        print(" | ".join(r))
        print("-" * 9)


def check_winner(b, p):
    for i in range(3):
        if all(b[i][j] == p for j in range(3)):
            return True
        if all(b[j][i] == p for j in range(3)):
            return True
    if all(b[i][i] == p for i in range(3)):
        return True
    if all(b[i][2-i] == p for i in range(3)):
        return True
    return False


def is_full(b):
    for r in b:
        for c in r:
            if c == " ":
                return False
    return True


def minimax(b, m):
    if check_winner(b, "X"):
        return 1
    if check_winner(b, "O"):
        return -1
    if is_full(b):
        return 0
    s = float("-inf") if m else float("inf")
    p = "X" if m else "O"
    for i in range(3):
        for j in range(3):
            if b[i][j] == " ":
                b[i][j] = p
                v = minimax(b, not m)
                b[i][j] = " "
                if m and v > s:
                    s = v
                if not m and v < s:
                    s = v
    return s


def best_move(b):
    s = float("-inf")
    m = None
    for i in range(3):
        for j in range(3):
            if b[i][j] == " ":
                b[i][j] = "X"
                v = minimax(b, False)
                b[i][j] = " "
                if v > s:
                    s = v
                    m = (i, j)
    return m


b = [[" "]*3 for _ in range(3)]
print("Tic-Tac-Toe: O=You, X=AI")
print_board(b)
while True:
    rc = input("Row Col (ex: 1 1): ").split(" ")
    r, c = int(rc[0]), int(rc[1])
    if 0 <= r < 3 and 0 <= c < 3 and b[r][c] == " ":
        b[r][c] = "O"
        print_board(b)
        if check_winner(b, "O"):
            print("You win!")
            break
        if is_full(b):
            print("Tie!")
            break
        m = best_move(b)
        if m:
            b[m[0]][m[1]] = "X"
        print("AI move:")
        print_board(b)
        if check_winner(b, "X"):
            print("AI wins!")
            break
        if is_full(b):
            print("Tie!")
            break
    else:
        print("Invalid")

'''

def getCode():
    global code
    print(code)
    