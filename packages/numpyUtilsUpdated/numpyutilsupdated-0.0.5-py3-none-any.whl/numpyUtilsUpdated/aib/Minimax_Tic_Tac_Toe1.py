code="""
import math

board = [' ' for i in range(9)]
human_player = 'X'
computer_player = 'O'

def print_board(board):
    for i in range(0, 9, 3):
        print("|".join(board[i:i+3]))

def get_empty_cells(board):
    return [i for i, cell in enumerate(board) if cell == ' ']

def is_winner(board, player):
    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]
    return any(all(board[i] == player for i in combo) for combo in winning_combinations)

def is_board_full(board):
    return ' ' not in board

def evaluate(board):
    if is_winner(board, computer_player):
        return 1
    elif is_winner(board, human_player):
        return -1
    else:
        return 0

def minimax(board, depth, maximizing_player):
    if depth == 0 or is_winner(board, human_player) or is_winner(board, computer_player) or is_board_full(board):
        return evaluate(board)
    
    if maximizing_player:
        max_eval = -math.inf
        for cell in get_empty_cells(board):
            board[cell] = computer_player
            eval = minimax(board, depth - 1, False)
            board[cell] = ' '
            max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = math.inf
        for cell in get_empty_cells(board):
            board[cell] = human_player
            eval = minimax(board, depth - 1, True)
            board[cell] = ' '
            min_eval = min(min_eval, eval)
        return min_eval

def find_best_move(board):
    best_eval = -math.inf
    best_move = -1
    for cell in get_empty_cells(board):
        board[cell] = computer_player
        eval = minimax(board, 9, False)
        board[cell] = ' '
        if eval > best_eval:
            best_eval = eval
            best_move = cell
    return best_move

def play_game():
    current_player = human_player
    while not is_winner(board, human_player) and not is_winner(board, computer_player) and not is_board_full(board):
        if current_player == human_player:
            print("Your turn (", human_player, ")")
            move = int(input("Enter your move (0-8): "))
            if move not in get_empty_cells(board):
                print("Invalid move. Try again.")
                continue
        else:
            print("Computer's turn (", computer_player, ")")
            move = find_best_move(board)
        
        board[move] = current_player
        print_board(board)
        current_player = human_player if current_player == computer_player else computer_player
    
    if is_winner(board, human_player):
        print("You win!")
    elif is_winner(board, computer_player):
        print("Computer wins!")
    else:
        print("It's a draw!")

print("Welcome to Tic Tac Toe!")
print("Here is the initial board:")
print_board(board)

play_game()
"""

def getCode():
    global code
    print(code)
    
 