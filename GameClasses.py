import numpy as np
import random


class State:
    def __init__(self, whitePieceCoordinates=[[5,1], [1,3], [1,4], [7,4], [7,5], [3,7]], blackPieceCoordinates=[(2,1), (3,1), (7,2), (1,6), (5,7), (6,7)]):
        np_white_pieces = np.array(whitePieceCoordinates).reshape(-1,2)
        np_black_pieces = np.array(blackPieceCoordinates).reshape(-1,2)
        self.pieces = np.vstack((np_white_pieces, np_black_pieces)) 
        
    def display(self):
        print("  x 1 2 3 4 5 6 7 ")
        print("y")
        for column in range(7):
            print(str(column+1) + "   ", end='')
            for row in range(7):
                try:
                    piece_index = np.where((self.pieces[:,0] == row+1) & (self.pieces[:,1] == column+1))[0][0]
                except IndexError:
                    print(" ,", end='')
                    continue
                if piece_index < len(self.pieces)/2:
                    print("O,", end='')
                else:
                    print("X,", end='')
            print("")
        print("")
        
    def isValidMove(self, move):
        #check that the move makes sense
        
        if np.all(move.oldCoordinates == move.newCoordinates) or not np.any(move.oldCoordinates == move.newCoordinates): return False
        if np.any(move.oldCoordinates < 1) or np.any(move.oldCoordinates > 7) or np.any(move.newCoordinates < 1) or np.any(move.newCoordinates > 7): return False
        
        #check that a piece is at oldCoordinates
        try:
            piece_index = np.where((self.pieces[:,0] == move.oldCoordinates[0]) & (self.pieces[:,1] == move.oldCoordinates[1]))[0][0]
        except IndexError:
            return False
        
        move_distance = max(abs(move.oldCoordinates[0] - move.newCoordinates[0]),abs(move.oldCoordinates[1] - move.newCoordinates[1]))
        
        if move.newCoordinates[0] - move.oldCoordinates[0] > 0: step_amt = np.array([1,0])
        elif move.newCoordinates[0] - move.oldCoordinates[0] < 0: step_amt = np.array([-1,0])
        elif move.newCoordinates[1] - move.oldCoordinates[1] > 0: step_amt = np.array([0,1])
        else: step_amt = np.array([0,-1])
        #check that no piece lies along the path to that square
        if self.numFreeSpaces(move.oldCoordinates, step_amt) < move_distance: return False
            
        #check that piece is able to be moved by desired amount
        if move_distance > self.numSquaresMovable(piece_index): return False
        
        return True
    
    def numFreeSpaces(self, start_coordinates, step_amt):
        i = start_coordinates + step_amt
        num_steps = 0
        while True:
            try:
                if np.any(i < 1) or np.any(i > 7) or num_steps == 3: return num_steps
                _ = np.where((self.pieces[:,0] == i[0]) & (self.pieces[:,1] == i[1]))[0][0]
                return num_steps
            except IndexError:
                i += step_amt
                num_steps += 1
                
    def numSquaresMovable(self, piece_index):
        if piece_index < len(self.pieces)/2:
            distances_to_other_pieces = np.linalg.norm(self.pieces[int(len(self.pieces)/2):] - np.array(self.pieces[piece_index]), axis=1)
        else:
            distances_to_other_pieces = np.linalg.norm(self.pieces[:int(len(self.pieces)/2)] - np.array(self.pieces[piece_index]), axis=1)
        close_pieces = distances_to_other_pieces < 2
        return 3 - np.count_nonzero(close_pieces)
    
    def update(self, move):
        if not self.isValidMove(move):
            print("Invalid move: " + str(move))
            exit()
        piece_index = np.where((self.pieces[:,0] == move.oldCoordinates[0]) & (self.pieces[:,1] == move.oldCoordinates[1]))[0][0]
        self.pieces[piece_index] = move.newCoordinates
        
    def getWinner(self):
        def isInSquare(piece, pieces):
            pieces_list = pieces.tolist()
            #check if square goes to top left of piece
            if (piece + np.array([0,-1])).tolist() in pieces_list \
                    and (piece + np.array([-1,-1])).tolist() in pieces_list \
                    and (piece + np.array([-1,0])).tolist() in pieces_list:
                return True
            #check if square goes to bottom left of piece
            if (piece + np.array([0,1])).tolist() in pieces_list \
                    and (piece + np.array([-1,1])).tolist() in pieces_list \
                    and (piece + np.array([-1,0])).tolist() in pieces_list:
                return True
            #check if square goes to top right of piece
            if (piece + np.array([0,-1])).tolist() in pieces_list \
                    and (piece + np.array([1,-1])).tolist() in pieces_list \
                    and (piece + np.array([1,0])).tolist() in pieces_list:
                return True
            #check if square goes to bottom right of piece
            if (piece + np.array([0,1])).tolist() in pieces_list \
                    and (piece + np.array([1,1])).tolist() in pieces_list \
                    and (piece + np.array([1,0])).tolist() in pieces_list:
                return True
            
        white_pieces = self.pieces[:int(len(self.pieces)/2)]
        for piece in white_pieces:
            if isInSquare(piece, white_pieces):
                print("win")
                self.display()
                return Color.white
        black_pieces = self.pieces[int(len(self.pieces)/2):]
        for piece in black_pieces:
            if isInSquare(piece, black_pieces):
                print("win")
                self.display()
                return Color.black
            
        return None
    
    def quality(self, color):
        winner = self.getWinner()
        if winner == color: return 1 # AGENT WIN
        elif winner is not None: return -1 # OPPONENT WIN
        else: #NO CLEAR WINNER
            return random.uniform(-1, 1)
        
    def possibleNextStates(self, color):
        if color == Color.white:
            movable_pieces = self.pieces[:int(len(self.pieces)/2)]
            i_offset = 0
        else:
            movable_pieces = self.pieces[int(len(self.pieces)/2):]
            i_offset = int(len(self.pieces)/2)
        
        possible_moves = []
        for i in range(len(movable_pieces)):
            max_move_dist_overall = self.numSquaresMovable(i+i_offset)
            for direction in [np.array([-1,0]), np.array([1,0]), np.array([0,-1]), np.array([0,1])]:
                max_move_dist = min(max_move_dist_overall, self.numFreeSpaces(movable_pieces[i], direction))
                for m in range(max_move_dist):
                    pieceCoordinatesAfterMove = movable_pieces[i] + direction * (m + 1)
                    possible_moves.append(Move(oldCoordinates=movable_pieces[i], newCoordinates=pieceCoordinatesAfterMove))
        
        possible_next_states = []    
        for move in possible_moves:
            possible_state = State()
            possible_state.pieces = np.copy(self.pieces)
            possible_state.update(move)
            possible_next_states.append(possible_state)
            
        return possible_next_states
    
    def getMoveToState(self, state):
        changed_piece_idx = np.where(state.pieces != self.pieces)[0][0]
        return Move(oldCoordinates=self.pieces[changed_piece_idx], newCoordinates=state.pieces[changed_piece_idx])
    
    def _reverseRows(self, pieces):
        new_pieces = np.zeros(pieces.shape)
        new_pieces[:, 0] = (pieces[:,0] * -1) + 8
        new_pieces[:, 1] = pieces[:,1]
        return new_pieces
    
    def _reverseColumns(self, pieces):
        new_pieces = np.zeros(pieces.shape)
        new_pieces[:, 0] = pieces[:,0]
        new_pieces[:, 1] = (pieces[:,1] * -1) + 8
        return new_pieces
    
    def _switchRowsAndColumns(self,pieces):
        new_pieces = np.zeros(pieces.shape)
        new_pieces[:, 0] = pieces[:,1]
        new_pieces[:, 1] = pieces[:,0]
        return new_pieces
    
    def isEquivalent(self, state):
        # Sort the pieces to be comparable
        sorted_pieces_a = np.vstack((np.sort(state.pieces[:int(len(state.pieces)/2)], axis=0), np.sort(state.pieces[int(len(state.pieces)/2):], axis=0)))
        sorted_pieces_b = np.vstack((np.sort(self.pieces[:int(len(self.pieces)/2)], axis=0), np.sort(self.pieces[int(len(self.pieces)/2):], axis=0)))
        # Compare the sorted piece arrays
        if np.array_equal(sorted_pieces_a, sorted_pieces_b): return True
        #check combinations of rotations + inverts
        for f_row in [lambda x: x, self._reverseRows]:
            for f_col in [lambda x: x, self._reverseColumns]:
                for f_rot in [lambda x: x, self._switchRowsAndColumns]:
                    if np.array_equal(f_rot(f_col(f_row(sorted_pieces_a))), sorted_pieces_b): return True
        return False
        
        
class Move:
    def __init__(self, oldCoordinates=None, newCoordinates=None, string=None):
        if string is not None:
            self.createFromString(string)
        else:
            self.oldCoordinates = np.array(oldCoordinates)
            self.newCoordinates = np.array(newCoordinates)
        
    def createFromString(self,string):
        try:
            piece_to_move_row = int(string[0])
            piece_to_move_col = int(string[1])
            move_direction = string[2]
            amount_to_move = int(string[3])
            if string[4] != '\n': raise Exception
        except:
            print("Received move is invalid:", list(string))
            exit()
        
        if move_direction == "W":
            piece_new_row = piece_to_move_row - amount_to_move
            piece_new_col = piece_to_move_col
        elif move_direction == "E":
            piece_new_row = piece_to_move_row + amount_to_move
            piece_new_col = piece_to_move_col
        elif move_direction == "N":
            piece_new_row = piece_to_move_row
            piece_new_col = piece_to_move_col - amount_to_move
        elif move_direction == "S":
            piece_new_row = piece_to_move_row
            piece_new_col = piece_to_move_col + amount_to_move
        else:
            print("Received move is invalid:", list(string))
            exit()
            
        self.oldCoordinates = np.array([piece_to_move_row, piece_to_move_col])
        self.newCoordinates = np.array([piece_new_row, piece_new_col])
        if np.all(self.oldCoordinates == self.newCoordinates) or not np.any(self.oldCoordinates == self.newCoordinates):
            print("Received move is invalid:", list(string))
            exit()
        return self
    
    def __str__(self):
        row_change = self.newCoordinates[0] - self.oldCoordinates[0]
        col_change = self.newCoordinates[1] - self.oldCoordinates[1]
        if col_change != 0:
            move_direction = "N" if col_change < 0 else "S"
        else:
            move_direction = "W" if row_change < 0 else "E"
            
        amount_to_move = max(abs(row_change), abs(col_change))
        moveString = str(self.oldCoordinates[0]) + str(self.oldCoordinates[1]) + move_direction + str(amount_to_move) + '\n'
        return moveString


class Color:
    white = "W"
    black = "B"
    def other(color):
        if color == "W": return "B"
        else: return "W"
        
    