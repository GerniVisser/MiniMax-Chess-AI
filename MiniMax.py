import chess
from Evaluation import Evalualtion

MAX, MIN = 100000, -100000

# Returns optimal value for current player
# (Initially called for root and maximizer)
def minimax(depth, maximizingPlayer, alpha, beta, board, firstMove, checkMate=False):

    boardString = board.fen()

    # Terminating condition. i.e
    # leaf node is reached
    if (depth == 0) or (checkMate):
        if maximizingPlayer:
            eval = Evalualtion(boardString, "B", checkMate)
        else:
            eval = Evalualtion(boardString, "W", checkMate)

        return eval.result()

    # All Code from here only runs if the tree has not yet reached the leaf node

    if maximizingPlayer:

        best = MIN

        # Recur for left and right children
        for i in board.legal_moves:

            board.push(i)

            mateWhite = False
            if board.is_checkmate():
                print(i)
                mateWhite = True
                #return MAX

            val = minimax(depth - 1, False, alpha, beta, board, False, mateWhite)

            board.pop()

            if val > best:
                best = val
                best_move_white = i

            alpha = max(alpha, best)

            # Alpha Beta Pruning
            if beta <= alpha:
                break

        if firstMove:
            #print("White best Move first " + str(best_move_white))
            return best_move_white
        else:
            #print("White best Move " + str(best_move_white))
            return best

    else:
        best = MAX

        # Recur for left and
        # right children
        #print(board.legal_moves)
        for i in board.legal_moves:

            board.push(i)

            mateBlack = False
            if board.is_checkmate():
                print(i)
                mateBlack = True
                #return MIN

            val = minimax(depth - 1, True, alpha, beta, board, False, mateBlack)

            board.pop()

            if val < best:
                best = val
                best_move_black = i


            beta = min(beta, best)

            # Alpha Beta Pruning
            if beta <= alpha:
                break

        if firstMove:
            #print("Black best Move first " + str(best_move_black))
            return best_move_black
        else:
            #print("Black best Move " + str(best_move_black))
            return best


#if __name__ == "__main__":
#    board = chess.Board()
#    for x in range(10):
#        white = minimax(3, MIN, MAX, board, True)
#        board.push(white)
#        print(board)
#        print(board.legal_moves)
#        board.push_san(input("Make Move"))

