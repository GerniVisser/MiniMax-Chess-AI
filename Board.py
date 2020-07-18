import pygame as py

class DisplayBoard():

    def __init__(self, board):

        # General Variables
        self.run = True
        self.dim = 500
        self.boardPos = {}
        self.boardLayout = {}
        self.selected_piece = None
        self.square_to_move_too = None


        # General pygame Init

        py.init()
        self.win = py.display.set_mode((self.dim, self.dim))
        py.display.set_caption("Chess")

        self.chessBoard = py.image.load("Image\Board.jpg").convert_alpha()
        self.chessBoard = py.transform.scale(self.chessBoard, (self.dim, self.dim))

        #Initialize the boardlayout
        for x in range(8):
            for y in range(8):
                # boardPos Initialized once only saves coordinate data about where the actual blocks are
                self.boardPos[str(chr(97 + x) + str(y + 1))] = [x * 51.5 + 45, 404 - y * 51]

                # Save the position in Chess Notation where different pieces are located wil dynamically change every move.
                # This only initializes the names of the different items in Dictionary
                self.boardLayout[str(chr(97 + x) + str(y + 1))] = None

        #Setup is only ran once to set the initial
        #self.setup()
        self.update(board)
        #self.update('rnbqkbn1/pppppppp/7r/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')


    def update(self, board):
        #Clear the boardLayout Dict so new one can be creates
        for x in range(8):
            for y in range(8):
                self.boardLayout[str(chr(97 + x) + str(y + 1))] = None

        #Gets rid of unnecessary data at end of string
        board = board[0:board.find(' ')]
        board = board + '/'

        #Basic String manipulation to determine where every piece on the board should be positioned
        for y in range(8, 0, -1):
            dash = board.find('/')
            rawCode = board[0:dash]
            board = board[dash+1:len(board)]

            alphabetCounter = 97
            for char in rawCode:
                if char.isdigit():
                    alphabetCounter += int(char)
                else:
                    self.boardLayout[str(chr(alphabetCounter)) + str(y)] = self.pieceData(char)
                    alphabetCounter +=1

    def pieceData(self, piece):
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
    # IF there was a piece already selected  the second  click is the block the selected piece should move to.
    def square_select(self, pos):
        x_board_pos = ((pos[0] - 45) // 50)
        y_board_pos = -((pos[1] - 405) // 50) + 1

        if self.selected_piece == None:
            self.square_to_move_too = None
            self.selected_piece = str(chr(97 + x_board_pos) + str(y_board_pos))
            return None

        else:
            self.square_to_move_too = str(chr(97 + x_board_pos) + str(y_board_pos))
            result = self.selected_piece+self.square_to_move_too
            self.square_to_move_too = None
            self.square_to_move_too = None
            return result


    # If RightClick the current selected Piece is set to None.
    def remove_square_select(self):
        self.selected_piece = None
        self.square_to_move_too = None






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


#test = DisplayBoard('rnbqkbn1/pppppppp/7r/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')









