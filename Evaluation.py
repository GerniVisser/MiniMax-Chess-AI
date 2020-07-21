from Piece_Development_Values import BoardValues

class Evalualtion():

    def __init__(self, board, color):
        self.board = board
        self.color = color
        self.boardValues = BoardValues()
        self.lateGameWhite = False
        self.lateGameBlack = False

        #Cretes empty BoardLayout list from where comparisons can be made.
        self.boardLayout = [None] * 64

        # Actually populate boardLayout with data from boardString.
        self.populate()

    def populate(self):

        boardString = self.board.fen()

        # Gets rid of unnecessary data at end of string
        boardString = boardString[0:boardString.find(' ')]
        boardString = boardString + '/'

        # Basic String manipulation to determine where every piece on the board should be positioned
        counter = 0

        for y in range(8):
            dash = boardString.find('/')
            rawCode = boardString[0:dash]
            boardString = boardString[dash + 1:len(boardString)]

            for char in rawCode:
                if char.isdigit():
                    counter += int(char)
                else:
                    self.boardLayout[counter] = char
                    counter += 1

    def materialComp(self):

        total = 0
        boardString = self.board.fen()

        # Gets rid of unnecessary data at end of string
        boardString = boardString[0:boardString.find(' ')]

        # Basic String manipulation to determine where every piece on the board should be positioned
        for i in boardString:
            if str(i) == "P": total += 100
            elif str(i) == "N": total += 320
            elif str(i) == "B": total += 330
            elif str(i) == "R": total += 500
            elif str(i) == "Q": total += 900
            elif str(i) == "K": total += 20000

            elif str(i) == "p": total -= 100
            elif str(i) == "n": total -= 320
            elif str(i) == "b": total -= 330
            elif str(i) == "r": total -= 500
            elif str(i) == "q": total -= 900
            elif str(i) == "k": total -= 20000
            else: pass

        return total

    def development(self):
        total = 0
        counter = 0
        # GamePos determines whether it is early or late game that determines how aggressive the king should be.
        # 1 Means it is Late game and 0 it is Early to mid Game.

        numberOfMinorPiecesWhite = 0
        numberOfMinorPiecesBlack = 0

        for piece in self.boardLayout:
            if piece != None:
                if str(piece) == "P":
                    total += self.boardValues.Pawn[-(counter-63)]
                elif str(piece) == "N":
                    total += self.boardValues.Knight[-(counter-63)]
                    numberOfMinorPiecesWhite += 1
                elif str(piece) == "B":
                    total += self.boardValues.Bishop[-(counter-63)]
                    numberOfMinorPiecesWhite += 1
                elif str(piece) == "R":
                    total += self.boardValues.Rook[-(counter-63)]
                    numberOfMinorPiecesWhite += 1
                elif str(piece) == "Q":
                    total += self.boardValues.Queen[-(counter-63)]
                    numberOfMinorPiecesWhite += 1

                #######################################################################

                elif str(piece) == "p":
                    total -= self.boardValues.Pawn[counter]
                elif str(piece) == "n":
                    total += self.boardValues.Knight[counter]
                    numberOfMinorPiecesBlack += 1
                elif str(piece) == "b":
                    total += self.boardValues.Bishop[counter]
                    numberOfMinorPiecesBlack += 1
                elif str(piece) == "r":
                    total += self.boardValues.Rook[counter]
                    numberOfMinorPiecesBlack += 1
                elif str(piece) == "q":
                    total += self.boardValues.Queen[counter]
                    numberOfMinorPiecesBlack += 1

            counter += 1

        counter = 0
        for piece in self.boardLayout:
            if piece != None:
                # If True it is still early game.
                if str(piece) == "k":
                    if (numberOfMinorPiecesBlack >= 3):
                        total += self.boardValues.KingEarly[counter]
                    else:
                        total += self.boardValues.KingLate[counter]
                        self.lateGameBlack = True
                        print("Black LAte")

                # If True it is still early game.
                elif str(piece) == "K":
                    if (numberOfMinorPiecesWhite >= 3):
                        total += self.boardValues.KingEarly[-(counter - 63)]
                    else:
                        total += self.boardValues.KingLate[-(counter - 63)]
                        self.lateGameWhite = True

            counter += 1

        return total

    def checkmate(self):

        total = 0

        if self.board.is_checkmate:
            if self.color == "W":
                total += 50000
            else:
                total -= 50000

        return total

    def is_late_game(self):
        self.development()
        if (self.lateGameBlack) and (self.lateGameWhite):
            return True
        else:
            return False

    def result(self):
        total = 0

        #1 Material Comp gives int val to board acording to what pieces is still on the board
        total += self.materialComp()

        #2 Develompent gives int val to board acording to where on board pieces is located uses Piece_Development_Values.py
        total += self.development()

        #3 Gives int value if the current move could put the opposite player in checkmate
        total += self.checkmate()

        return total

