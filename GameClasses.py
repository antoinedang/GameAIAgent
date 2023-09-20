import numpy as np
from itertools import combinations
from math import sqrt

class State:
    def __init__(self, whitePieceCoordinates=[[5,1], [1,3], [1,4], [7,4], [7,5], [3,7]], blackPieceCoordinates=[(2,1), (3,1), (7,2), (1,6), (5,7), (6,7)], ignoreSetup=False):
        if ignoreSetup: return
        np_white_pieces = np.array(whitePieceCoordinates).reshape(-1,2)
        np_black_pieces = np.array(blackPieceCoordinates).reshape(-1,2)
        self.pieces = np.vstack((np_white_pieces, np_black_pieces)) 
        self.white_piece_count = int(len(self.pieces)/2)
        
    def display(self):
        print("  x 1 2 3 4 5 6 7 ")
        print("y")
        for column in range(7):
            print(str(column+1) + "   ", end='')
            for row in range(7):
                piece_index = self.getPieceIndexByCoordinates(row+1, column+1)
                if piece_index == -1:
                    print(" ,", end='')
                    continue
                if piece_index < self.white_piece_count:
                    print("O,", end='')
                else:
                    print("X,", end='')
            print("")
        print("")
        
    def isValidMove(self, move):
        #check that the move makes sense
        
        if (self.oldCoordinates[0] == self.newCoordinates[0] and self.oldCoordinates[1] == self.newCoordinates[1]) \
            or (self.oldCoordinates[0] != self.newCoordinates[0] and self.oldCoordinates[1] != self.newCoordinates[1]): return False
        if move.oldCoordinates[0] < 1 or move.oldCoordinates[1] < 1 \
            or move.oldCoordinates[0] > 7 or move.oldCoordinates[1] > 7 \
                or move.newCoordinates[0] < 1 or move.newCoordinates[1] < 1 \
                    or move.newCoordinates[0] > 7 or move.newCoordinates[1] > 7: return False
        
        #check that a piece is at oldCoordinates
        piece_index = self.getPieceIndexByCoordinates(self,move.oldCoordinates[0],move.oldCoordinates[1])
        if piece_index < 0: return False
        
        
        move_distance = max(abs(move.oldCoordinates[0] - move.newCoordinates[0]),abs(move.oldCoordinates[1] - move.newCoordinates[1]))
        
        if move.newCoordinates[0] - move.oldCoordinates[0] > 0: step_amt = directions[1]
        elif move.newCoordinates[0] - move.oldCoordinates[0] < 0: step_amt = directions[0]
        elif move.newCoordinates[1] - move.oldCoordinates[1] > 0: step_amt = directions[3]
        else: step_amt = directions[2]
        #check that no piece lies along the path to that square
        if self.numFreeSquaresInDirection(move.oldCoordinates, step_amt) < move_distance: return False
            
        #check that piece is able to be moved by desired amount
        if move_distance > self.numSquaresMovable(piece_index): return False
        
        return True
    
    def numFreeSquaresInDirection(self, start_coordinates, step_amt): # TODO?
        i = start_coordinates + step_amt
        pieces_list = self.pieces.tolist()
        num_steps = 0
        while True:
            if i[0] < 1 or i[1] < 1 or i[0] > 7 or i[1] > 7 or num_steps >= 3 or i.tolist() in pieces_list:
                return num_steps
            else:
                i += step_amt
                num_steps += 1
                
    def numSquaresMovable(self, piece_index):
        if piece_index < self.white_piece_count:
            distances_to_other_pieces = np.linalg.norm(self.pieces[self.white_piece_count:] - self.pieces[piece_index], axis=1)
        else:
            distances_to_other_pieces = np.linalg.norm(self.pieces[:self.white_piece_count] - self.pieces[piece_index], axis=1)
        close_pieces = distances_to_other_pieces < 2
        return max(3 - np.count_nonzero(close_pieces), 0)
    
    def update(self, move, check_validity=False):
        if check_validity and not self.isValidMove(move):
            print("Invalid move: " + str(move))
            exit()
        piece_index = self.getPieceIndexByCoordinates(move.oldCoordinates[0],move.oldCoordinates[1])
        self.pieces[piece_index] = move.newCoordinates
        
    def getWinner(self): # TODO
        for pieces in combinations(self.pieces[:self.white_piece_count], 4):
            if _formsSquare(pieces): return Color.white
        for pieces in combinations(self.pieces[self.white_piece_count:], 4):
            if _formsSquare(pieces): return Color.black
            
        return None
        
    def quality(self, color, depth, winner=-1): # TODO
        if winner == -1: winner = self.getWinner()
        if winner == color: return 10/depth # AGENT WIN
        elif winner is not None: return -10/depth # OPPONENT WIN
        else: #NO CLEAR WINNER
            #simple heuristic: approx. distance between agent pieces minus approx. distance between opponent pieces
            if color == Color.white:
                our_pieces = self.pieces[:self.white_piece_count]
                opponent_pieces = self.pieces[self.white_piece_count:]
            else:
                our_pieces = self.pieces[self.white_piece_count:]
                opponent_pieces = self.pieces[:self.white_piece_count]
                
            #we can approximate this by getting the standard deviation of the x and y coordinates of our pieces
            our_std_avg = 1 - (_variance(our_pieces[:,0]) + _variance(our_pieces[:,1])) / (2*7)
            opponent_std_avg = -1 * (1 - (_variance(opponent_pieces[:,0]) + _variance(opponent_pieces[:,1])) / (2*7))
            return our_std_avg + opponent_std_avg

    def possibleNextStates(self, color): # TODO
        if color == Color.white:
            movable_pieces = self.pieces[:self.white_piece_count]
            enemy_pieces = self.pieces[self.white_piece_count:]
            i_offset = 0
        else:
            movable_pieces = self.pieces[self.white_piece_count:]
            enemy_pieces = self.pieces[:self.white_piece_count]
            i_offset = self.white_piece_count
            
        pieces_list = self.pieces.tolist()
        
        possible_next_states = []
        for i in range(self.white_piece_count):
            movable_piece = movable_pieces[i]
            max_move_dist = 3
            for e in enemy_pieces:
                dist = sqrt((e[0]-movable_piece[0])**2 + (e[1]-movable_piece[1])**2)
                if dist < 2:
                    max_move_dist -= 1
                    if max_move_dist == 0: break
            if max_move_dist == 0: continue
            for direction in directions:
                pieceCoordinatesAfterMove = [movable_piece[0], movable_piece[1]]
                for _ in range(max_move_dist):
                    pieceCoordinatesAfterMove[0] += direction[0]
                    pieceCoordinatesAfterMove[1] += direction[1]
                    if pieceCoordinatesAfterMove[0] < 1 or pieceCoordinatesAfterMove[1] < 1 \
                        or pieceCoordinatesAfterMove[0] > 7 or pieceCoordinatesAfterMove[1] > 7 \
                            or pieceCoordinatesAfterMove in pieces_list: break
                    
                    possible_state = State(ignoreSetup=True)
                    possible_state.pieces = np.array(self.pieces, order='K', copy=True)
                    possible_state.pieces[i+i_offset][0] = pieceCoordinatesAfterMove[0]
                    possible_state.pieces[i+i_offset][1] = pieceCoordinatesAfterMove[1]
                    possible_state.white_piece_count = self.white_piece_count
                    
                    possible_next_states.append(possible_state)
        
        return possible_next_states
    
    def getPieceIndexByCoordinates(self,x,y):
        try:
            return self.pieces.tolist().index([x,y])
        except ValueError:
            return -1
    
    def getMoveToState(self, state):
        for i in range(len(self.pieces)):
            if self.pieces[i][0] != state.pieces[i][0] or self.pieces[i][1] != state.pieces[i][1]:
                changed_piece_idx = i
                break
        return Move(oldCoordinates=self.pieces[changed_piece_idx], newCoordinates=state.pieces[changed_piece_idx])        


class Move:
    def __init__(self, oldCoordinates=None, newCoordinates=None, string=None):
        if string is not None:
            self.createFromString(string)
        elif isinstance(oldCoordinates, np.ndarray) and isinstance(newCoordinates, np.ndarray):
            self.oldCoordinates = oldCoordinates
            self.newCoordinates = newCoordinates
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
        if (self.oldCoordinates[0] == self.newCoordinates[0] and self.oldCoordinates[1] == self.newCoordinates[1]) or (self.oldCoordinates[0] != self.newCoordinates[0] and self.oldCoordinates[1] != self.newCoordinates[1]):
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


def _variance(x):
    n = len(x)
    mean = sum(x) / n
    return sum((x - mean) ** 2 for x in x) / n

def _formsSquare(pieces):
    min_x = 8
    max_x = 0
    min_y = 8
    max_y = 0
    for piece in pieces:
        x,y = piece
        if x > max_x: max_x = x
        if x < min_x: min_x = x
        if y > max_y: max_y = y
        if y < min_y: min_y = y
    
    return (max_x - min_x) == 1 and (max_y - min_y) == 1

#global variables for performance: no need to instantiate these every time since they are constant
directions = [np.array([-1,0]), np.array([1,0]), np.array([0,-1]), np.array([0,1])]
move_obj = Move(oldCoordinates=[0,0], newCoordinates=[0,0])