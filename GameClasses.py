class State:
    def __init__(self, whitePieceCoordinates=[(5,1), (1,3), (1,4), (7,4), (7,5), (3,7)], blackPieceCoordinates=[(2,1), (3,1), (7,2), (1,6), (5,7), (6,7)]):
        self.pieces = whitePieceCoordinates + blackPieceCoordinates
    def display(self):
        print("    1 2 3 4 5 6 7 ")
        print("")
        for column in range(7):
            print(str(column+1) + "   ", end='')
            for row in range(7):
                try:
                    piece_index = self.pieces.index((row+1, column+1))
                except ValueError:
                    piece_index = -1
                if piece_index == -1:
                    print(" ,", end='')
                elif piece_index < 6:
                    print("O,", end='')
                else:
                    print("X,", end='')
            print("")
        print("")
    def isValidMove(self, move):
        pass
    def update(self, move):
        if not self.isValidMove(move):
            print("Invalid move: " + str(move))
            exit()
        piece_index = self.pieces.index(move.oldCoordinates)
        self.pieces[piece_index] = move.newCoordinates
    def getWinner(self):
        pass
    def quality(self, color):
        winner = self.getWinner()
        if winner == color:
            return 1
        elif winner is None:
            return 0
        else:
            return -1
    def possibleNextStates(self, color):
        pass
    def getMoveToState(self, state):
        pass
        
        
    
class Move:
    def __init__(self, oldCoordinates=None, newCoordinates=None, string=None):
        self.oldCoordinates = oldCoordinates
        self.newCoordinates = newCoordinates
        if string is not None:
            self.createFromString(string)
        
    def createFromString(self,string):
        piece_to_move_row = int(string[0])
        piece_to_move_col = int(string[1])
        move_direction = string[2]
        amount_to_move = int(string[3])
        
        if move_direction == "W":
            piece_new_row = piece_to_move_row - amount_to_move
            piece_new_col = piece_to_move_col
        elif move_direction == "E":
            piece_new_row = piece_to_move_row + amount_to_move
            piece_new_col = piece_to_move_col
        elif move_direction == "N":
            piece_new_row = piece_to_move_row
            piece_new_col = piece_to_move_col - amount_to_move
        else:
            piece_new_row = piece_to_move_row
            piece_new_col = piece_to_move_col + amount_to_move
            
        self.oldCoordinates = (piece_to_move_row, piece_to_move_col)
        self.newCoordinates = (piece_new_row, piece_new_col)
        return self
    
    def __str__(self):
        row_change = self.newCoordinates[0] - self.oldCoordinates[0]
        col_change = self.newCoordinates[1] - self.oldCoordinates[1]
        amount_to_move = max(row_change, col_change)
        if col_change != 0:
            move_direction = "N" if col_change < 0 else "S"
        else:
            move_direction = "E" if col_change < 0 else "W"
            
        moveString = str(self.oldCoordinates[0]) + str(self.oldCoordinates[1]) + move_direction + str(amount_to_move) + '\n'
        return moveString

class Color:
    white = "W"
    black = "B"
    