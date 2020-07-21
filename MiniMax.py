from Evaluation import Evalualtion

MAX, MIN = 100000, -100000

# Returns optimal value for current player
# (Initially called for root and maximizer)
def minimax(depth, maximizingPlayer, alpha, beta, board, firstMove):

    # Terminating condition. i.e
    # leaf node is reached
    if (depth == 0) or (board.is_game_over()):

        if maximizingPlayer:
            eval = Evalualtion(board, "W")
        else:
            eval = Evalualtion(board, "B")

        return eval.result()

    # All Code from here only runs if the tree has not yet reached the leaf node

    if maximizingPlayer:

        best = MIN
        # Recur for left and right children
        for i in board.legal_moves:

            board.push(i)

            if checkmate(board) and firstMove:
                return i

            val = minimax(depth - 1, False, alpha, beta, board, False)
            board.pop()

            if val > best:
                best = val
                best_move_white = i

            alpha = max(alpha, best)

            # Alpha Beta Pruning
            if beta <= alpha:
                break

        if firstMove:
            print(best_move_white)
            return best_move_white
        else:
            return best

    else:

        best = MAX
        for i in board.legal_moves:

            board.push(i)

            if checkmate(board) and firstMove:
                return i

            val = minimax(depth - 1, True, alpha, beta, board, False)
            board.pop()

            if val < best:
                best = val
                best_move_black = i

            beta = min(beta, best)

            # Alpha Beta Pruning
            if beta <= alpha:
                break

        if firstMove:
            return best_move_black
        else:
            return best

def checkmate(board):
    if board.is_checkmate():
        return True
    else:
        return False




