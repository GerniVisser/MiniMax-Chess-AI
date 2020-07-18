from Board import DisplayBoard
from MiniMax import minimax
import chess
import pygame as py

MAX, MIN = 100000, -100000

board = chess.Board()
fen = board.fen()

display = DisplayBoard(fen)

clock = py.time.Clock()

def makeMoveWhite(move):

    if player_color == "W":

        board.push_uci(move)
        pass
    else:
        white = minimax(4, True, MIN, MAX, board, True)
        #print(white)
        board.push(white)
    render_pieces()

def makeMoveBlack(move):

    if player_color == "B":
    #     print(board.legal_moves)
        board.push_uci(move)

    else:
        black = minimax(4, False, MIN, MAX, board, True)
        board.push(black)
    render_pieces()

def render_pieces():
    for num in display.boardLayout:
        if display.boardLayout[num] != None:
            display.win.blit(display.boardLayout[num].render(), (display.boardPos[num][0], display.boardPos[num][1]))

player_color = input("What color do you want to be enter 'W' for white and 'B' for black")


while display.run:

    if board.is_game_over():
        print("GAME OVER")

    events = py.event.get()
    for event in events:
        if event.type == py.QUIT:
            exit()

        if event.type == py.MOUSEBUTTONDOWN and event.button == 1:
            player_possible_move = display.square_select(py.mouse.get_pos())
            if player_possible_move != None:
                try:
                    makeMoveWhite(player_possible_move)
                    makeMoveBlack(player_possible_move)
                except:
                    print("Invalid Move")

        elif event.type == py.MOUSEBUTTONDOWN and event.button == 3:
            display.remove_square_select()


    #print(py.mouse.get_pos())

    display.update(board.fen())

    # Cycling through BoardLayout to render pieces left on board

    display.win.blit(display.chessBoard, (0, 0))

    render_pieces()

    py.display.update()
    clock.tick(10)


py.quit()

