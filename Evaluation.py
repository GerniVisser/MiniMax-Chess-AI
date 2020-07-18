from Piece_Developmet_Values import BoardValues

class Evalualtion():

    def __init__(self, boardString, color, checkMate=False):
        self.boardString = boardString
        self.color = color
        self.boardValues = BoardValues()
        self.lateGameWhite = False
        self.lateGameBlack = False
        self.checkMate = checkMate

        #Cretes empty BoardLayout list from where comparisons can be made.
        self.boardLayout = [None] * 64

        # Actually populater boardLayout with data from boardString.
        self.populate()

    def materialComp(self):
        total = 0
        white_total = 0
        black_total = 0
        # Gets rid of unnecessary data at end of string
        board = self.boardString[0:self.boardString.find(' ')]

        # Basic String manipulation to determine where every piece on the board should be positioned
        for i in board:
            if str(i) == "P": white_total += 100
            elif str(i) == "N": white_total += 320
            elif str(i) == "B": white_total += 330
            elif str(i) == "R": white_total += 500
            elif str(i) == "Q": white_total += 900
            elif str(i) == "K": white_total += 20000

            elif str(i) == "p": black_total -= 100
            elif str(i) == "n": black_total -= 320
            elif str(i) == "b": black_total -= 330
            elif str(i) == "r": black_total -= 500
            elif str(i) == "q": black_total -= 900
            elif str(i) == "k": black_total -= 20000
            else: pass

            total = white_total + black_total

        return total

    #TODO This Populate function could run in a diffened Thread I think it would thake a bit of processing and some of the checks like Material comp could run in Paralell to this.
    def populate(self):

        # Gets rid of unnecessary data at end of string
        board = self.boardString[0:self.boardString.find(' ')]
        board = board + '/'

        # Basic String manipulation to determine where every piece on the board should be positioned
        counter = 0
        for y in range(8):
            dash = board.find('/')
            rawCode = board[0:dash]
            board = board[dash + 1:len(board)]

            for char in rawCode:
                if char.isdigit():
                    counter += int(char)
                else:
                    self.boardLayout[counter] = char
                    counter += 1

        #print(self.boardLayout)

    def development(self):
        white_total = 0
        black_total = 0
        counter = 0
        # GamePos determines whether it is early or late game that determines how aggressive the king should be.
        # 1 Means it is Late game and 0 it is Early to mid Game.

        numberOfMinorPiecesWhite = 0
        numberOfMinorPiecesBlack = 0

        for piece in self.boardLayout:
            if piece != None:
                if str(piece) == "P":
                    white_total += self.boardValues.Pawn[-(counter-63)]
                elif str(piece) == "N":
                    white_total += self.boardValues.Knight[-(counter-63)]
                    numberOfMinorPiecesWhite += 1
                elif str(piece) == "B":
                    white_total += self.boardValues.Bishop[-(counter-63)]
                    numberOfMinorPiecesWhite += 1
                elif str(piece) == "R":
                    white_total += self.boardValues.Rook[-(counter-63)]
                    numberOfMinorPiecesWhite += 1
                elif str(piece) == "Q":
                    white_total += self.boardValues.Queen[-(counter-63)]
                    numberOfMinorPiecesWhite += 2

                elif str(piece) == "K":
                    # If True it is still early game.
                    if (numberOfMinorPiecesWhite >= 4):
                        white_total += self.boardValues.KingEarly[-(counter-63)]
                    else:
                        white_total += self.boardValues.KingLate[-(counter-63)]
                        self.lateGameWhite = True

                #######################################################################

                elif str(piece) == "p":
                    black_total -= self.boardValues.Pawn[counter]
                elif str(piece) == "n":
                    black_total += self.boardValues.Knight[counter]
                    numberOfMinorPiecesBlack += 1
                elif str(piece) == "b":
                    black_total += self.boardValues.Bishop[counter]
                    numberOfMinorPiecesBlack += 1
                elif str(piece) == "r":
                    black_total += self.boardValues.Rook[counter]
                    numberOfMinorPiecesBlack += 1
                elif str(piece) == "q":
                    black_total += self.boardValues.Queen[counter]
                    numberOfMinorPiecesBlack += 2

                elif str(piece) == "k":
                    # If True it is still early game.
                    if (numberOfMinorPiecesBlack >= 4):
                        black_total += self.boardValues.KingEarly[counter]
                    else:
                        black_total += self.boardValues.KingLate[counter]
                        self.lateGameBlack = True

            counter += 1

        total = white_total + black_total

        return total


    def result(self):
        total = 0
        total += self.materialComp()
        #print(total)

        total += self.development()
        #print(total)

        if self.color == "W":
            if self.checkMate:
                return 999999
            else:
            #print(total)
                return total
        else:
            if self.checkMate:
                return -999999
            else:
            #print(-total)
                return -total



#test = Evalualtion("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPP/RNBQKBNR w KQkq - 0 1",'W')
#print(test.result())
