code = '''
import math
def alpha_beta_pruning(index, depth, alpha, beta, maximizing_player):
    if depth == 0 or index >= len(scores):
        return scores[index] if index < len(scores) else 0


    left_index, right_index = 2 * index, 2 * index + 1


    if maximizing_player:
        max_eval = -float('inf')
        for child_index in [left_index, right_index]:
            if child_index < len(scores):
                ab_val = alpha_beta_pruning(child_index, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, ab_val)
                alpha = max(alpha, max_eval)
                if beta <= alpha:
                    break
        return max_eval
    else:
        min_eval = float('inf')
        for child_index in [left_index, right_index]:
            if child_index < len(scores):
                ab_val = alpha_beta_pruning(child_index, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, ab_val)
                beta = min(beta, min_eval)
                if beta <= alpha:
                    break
        return min_eval


scores = list(map(int, input("Enter Scores: ").split()))
depth = int(math.log2(len(scores)))
print("The Optimal Value is:", alpha_beta_pruning(0, depth, -float('inf'), float('inf'), True))

'''

def getCode():
    global code
    print(code)
    