from Board import DisplayBoard
from MiniMax import minimax
from Evaluation import Evalualtion
import chess
import pygame as py

# General variables
MAX, MIN = 100000, -100000
depth = 4

board = chess.Board()
display = DisplayBoard(board)

# Tis function can be run at anytime and wit completely reset the game.
def setup_game():
    board.reset_board()
    display.main_menu()
    display.update(board)
    run()

def move():
    player_possible_move = display.square_select(py.mouse.get_pos())
    if player_possible_move != None:
        try:
            eval = Evalualtion(board, display.player_color)
            is_late_game = eval.is_late_game()

            if display.player_color == "W":
                makeMoveWhite(player_possible_move, is_late_game)
                makeMoveBlack(player_possible_move, is_late_game)
            else:
                makeMoveBlack(player_possible_move, is_late_game)
                makeMoveWhite(player_possible_move, is_late_game)
        except:
            print("Invalid Move")

def makeMoveWhite(move, is_late_game):

    if display.player_color == "W":
        board.push_uci(move)
    else:
        # The depth attribute has to be odd
        if is_late_game:
            white = minimax(depth + 1, True, MIN, MAX, board, True)
        else:
            white = minimax(depth + 1, True, MIN, MAX, board, True)

        board.push(white)

    display.update(board)

def makeMoveBlack(move, is_late_game):

    if display.player_color == "B":
        board.push_uci(move)
    else:
        # The depth attribute has to be even
        if is_late_game:
            black = minimax(depth + 2, False, MIN, MAX, board, True)
        else:
            black = minimax(depth, False, MIN, MAX, board, True)
        board.push(black)

    display.update(board)

def is_game_over(board):
    if board.is_game_over():
        display.run = False
        display.game_over = True
        display.game_over_menu()

def run():

    if display.player_color == "B":
        makeMoveWhite(None, False)

    while display.run:
        events = py.event.get()
        for event in events:
            if event.type == py.QUIT:
                exit()

            if event.type == py.MOUSEBUTTONDOWN and event.button == 1:
                move()
            elif event.type == py.MOUSEBUTTONDOWN and event.button == 3:
                display.remove_square_select()

        display.update_screen()
        is_game_over(board)

while run:
    setup_game()

py.quit()


