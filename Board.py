import pygame as py
import chess

class DisplayBoard():

    def __init__(self, board):

        # General Variables
        self.run = False
        self.intro = True
        self.game_over = False
        self.dim = 500
        self.boardPos = {}
        self.boardLayout = {}
        self.show_moves_surf_list = []
        self.selected_square = None
        self.square_to_move_too = None
        self.player_color = None
        self.clock = py.time.Clock()
        self.board = board
        self.fen = board.fen()

        # General pygame Init

        py.init()
        self.win = py.display.set_mode((self.dim, self.dim))
        py.display.set_caption("Chess")
        # Create a surface for the chessboard itself
        self.chessBoard = py.image.load("Image\Board.jpg").convert_alpha()
        self.chessBoard = py.transform.scale(self.chessBoard, (self.dim, self.dim))

        self.show_moves_surf = py.Surface((50, 50), py.SRCALPHA, 32)
        py.draw.circle(self.show_moves_surf, (0, 200, 0, 100), (25, 25), 20, 0)

        self.boardlayout_init()

        #Setup is only ran once to set the initial
        self.update(self.board)


    def boardlayout_init(self):

        # Initialize the boardLayout dict
        for x in range(8):
            for y in range(8):
                # boardPos Initialized once only saves coordinate data about where the actual blocks are
                self.boardPos[str(chr(97 + x) + str(y + 1))] = [x * 51.5 + 46, 405 - y * 51]

                # Save the position in Chess Notation where different pieces are located wil dynamically change every move.
                # This only initializes the names of the different items in Dictionary
                self.boardLayout[str(chr(97 + x) + str(y + 1))] = None

    def update(self, board):
        # Clear the boardLayout Dict so new one can be created
        for x in range(8):
            for y in range(8):
                self.boardLayout[str(chr(97 + x) + str(y + 1))] = None

        self.board = board
        self.fen = board.fen()

        #Gets rid of unnecessary data at end of string
        boardString = str(self.fen)[0:str(self.fen).find(' ')]
        boardString = boardString + '/'

        #Basic String manipulation to determine where every piece on the board should be positioned
        for y in range(8, 0, -1):
            dash = boardString.find('/')
            rawCode = boardString[0:dash]
            boardString = boardString[dash + 1:len(boardString)]

            alphabetCounter = 97
            for char in rawCode:
                if char.isdigit():
                    alphabetCounter += int(char)
                else:
                    self.boardLayout[str(chr(alphabetCounter)) + str(y)] = self.pieceData(char)
                    alphabetCounter +=1
        self.update_screen()


    def update_screen(self):
        # This function updates the screen should be run every time a change is made to the board state
        self.win.blit(self.chessBoard, (0, 0))
        # Display all pieces in BoardLayout
        for num in self.boardLayout:
            if self.boardLayout[num] != None:
                self.win.blit(self.boardLayout[num].render(), (self.boardPos[num][0], self.boardPos[num][1]))
        # Displays circles that show possible moves
        if self.show_moves_surf_list != []:
            for num in self.show_moves_surf_list:
                self.win.blit(self.show_moves_surf, (num[0], num[1]))

        py.display.update()
        self.clock.tick(10)

    def update_possible_moves(self):
        # This functions updates where the littler circles appear that show player where certain piece can move
        if self.selected_square != None:
            self.show_moves_surf_list.clear()
            lg = self.board.legal_moves
            for pos in lg:
                if str(pos)[0:2] == self.selected_square:
                    self.show_moves_surf_list.append((self.boardPos[str(pos)[2:4]][0], self.boardPos[str(pos)[2:4]][1]))

    def pieceData(self, piece):

        # This class gets referenced when initializing new Pieces using Pieces class
        if piece == 'p': return Piece("Pawn", "B")
        elif piece == 'r': return Piece("Rook", "B")
        elif piece == 'n': return Piece("Knight", "B")
        elif piece == 'b': return Piece("Bishop", "B")
        elif piece == 'k': return Piece("King", "B")
        elif piece == 'q': return Piece("Queen", "B")

        elif piece == 'P': return Piece("Pawn", "W")
        elif piece == 'R': return Piece("Rook", "W")
        elif piece == 'N': return Piece("Knight", "W")
        elif piece == 'B': return Piece("Bishop", "W")
        elif piece == 'K': return Piece("King", "W")
        elif piece == 'Q': return Piece("Queen", "W")


    # If the player Left Click on block the piece on that block is the one to be moved.
    # If there was a piece already selected  the second  click is the block the selected piece should move to.
    # Except if the second click is on a Piece of same cloro then that piece becomes the Pieced to be movesd
    def square_select(self, pos):
        x_board_pos = ((pos[0] - 45) // 50)
        y_board_pos = -((pos[1] - 405) // 50) + 1
        # Set piece to be moved
        if self.selected_square == None:
            self.square_to_move_too = None
            self.selected_square = str(chr(97 + x_board_pos) + str(y_board_pos))
            self.update_possible_moves()
            return None

        else:
            self.square_to_move_too = str(chr(97 + x_board_pos) + str(y_board_pos))
            result = str(self.selected_square + self.square_to_move_too)
            for move in self.board.legal_moves:
                if str(move) == str(result + "q"):
                    self.remove_square_select()
                    return str(result + "q")
                elif str(move) == result:
                    self.remove_square_select()
                    return result

            if self.boardLayout[str(chr(97 + x_board_pos) + str(y_board_pos))] != None:
                self.square_to_move_too = None
                self.selected_square = str(chr(97 + x_board_pos) + str(y_board_pos))
                self.update_possible_moves()
                return None

    # If RightClick the current selected Piece is set to None.
    def remove_square_select(self):
        self.selected_square = None
        self.square_to_move_too = None
        self.show_moves_surf_list = []


############################################################################################################################
# From here is only UI stuff to display menus and buttons ect.

    def main_menu(self):

        red = (200, 0, 0)
        green = (0, 200, 0)

        bright_red = (255, 0, 0)
        bright_green = (0, 255, 0)

        while self.intro:
            for event in py.event.get():
                # print(event)
                if event.type == py.QUIT:
                    py.quit()

            self.win.fill((255,255,255))
            largeText = py.font.SysFont("comicsansms", 115)
            TextSurf, TextRect = self.text_objects("Chess", largeText)
            TextRect.center = ((self.dim / 2), (self.dim / 2 - 100))
            self.win.blit(TextSurf, TextRect)

            self.button("WHITE", 50, 300, 100, 50, green, bright_green, 1)
            self.button("BLACK", 350, 300, 100, 50, green, bright_green, 2)
            self.button("Quit", 225, 400, 80, 50, red, bright_red, 3)

            py.display.update()
            self.clock.tick(15)

    def game_over_menu(self):

        red = (200, 0, 0)
        green = (0, 200, 0)

        bright_red = (255, 0, 0)
        bright_green = (0, 255, 0)

        while self.game_over:
            for event in py.event.get():
                # print(event)
                if event.type == py.QUIT:
                    py.quit()

            self.win.fill((255,255,255,100))
            largeText = py.font.SysFont("comicsansms", 90)
            mediumText = py.font.SysFont("comicsansms", 50)
            TextSurfMian, TextRectMain = self.text_objects("Game Over", largeText)
            TextRectMain.center = ((self.dim / 2), (self.dim / 2 - 120))
            self.win.blit(TextSurfMian, TextRectMain)

            if self.board.turn == chess.WHITE:
                TextSurf, TextRect = self.text_objects("Black Won", mediumText)
            else:
                TextSurf, TextRect = self.text_objects("White Won", mediumText)

            TextRect.center = ((self.dim / 2), (self.dim / 2) - 20)
            self.win.blit(TextSurf, TextRect)

            self.button("Play Again", 225, 300, 100, 50, green, bright_green, 4)
            self.button("Quit", 225, 400, 100, 50, red, bright_red, 3)

            py.display.update()
            self.clock.tick(15)

    def button(self, msg, x, y, w, h, ic, ac, action=None):
        mouse = py.mouse.get_pos()
        click = py.mouse.get_pressed()
        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            py.draw.rect(self.win, ac, (x, y, w, h))

            if click[0] == 1 and action != None:
                if action == 1:
                    self.player_color = "W"
                    self.run = True
                    self.intro = False
                    self.game_over = False
                elif action == 2:
                    self.player_color = "B"
                    self.run = True
                    self.intro = False
                    self.game_over = False
                elif action == 3:
                    py.quit()
                elif action == 4:
                    self.run = False
                    self.intro = True
                    self.game_over = False

        else:
            py.draw.rect(self.win, ic, (x, y, w, h))

        smallText = py.font.SysFont("comicsansms", 20)
        textSurf, textRect = self.text_objects(msg, smallText)
        textRect.center = ((x + (w / 2)), (y + (h / 2)))
        self.win.blit(textSurf, textRect)

    def text_objects(self, text, font):
        textSurface = font.render(text, True, (0,0,0))
        return textSurface, textSurface.get_rect()

# This class is used to create Pieces and assign a Surface and Image to them
class Piece():

    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.dim = 45

        if (self.color == "W") or (self.color == "White"):
            if self.name != "Knight":
                self.pieceSurface = py.image.load("Image\Chess_"+self.name.lower()[0]+"lt60.png")
            else:
                self.pieceSurface = py.image.load("Image\Chess_nlt60.png")
        else:
            if self.name != "Knight":
                self.pieceSurface = py.image.load("Image\Chess_" + self.name.lower()[0] + "dt60.png")
            else:
                self.pieceSurface = py.image.load("Image\Chess_ndt60.png")

        self.pieceSurface = py.transform.scale(self.pieceSurface, (self.dim, self.dim))


    def render(self):
        return self.pieceSurface










