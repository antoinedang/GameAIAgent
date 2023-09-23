import numpy as np
import pickle
import numba as nb

class State:
    def __init__(self, whitePieceCoordinates=[[5,1], [1,3], [1,4], [7,4], [7,5], [3,7]], blackPieceCoordinates=[(2,1), (3,1), (7,2), (1,6), (5,7), (6,7)], ignoreSetup=False):
        if ignoreSetup: return
        np_white_pieces = np.array(whitePieceCoordinates).reshape(-1,2)
        np_black_pieces = np.array(blackPieceCoordinates).reshape(-1,2)
        self.pieces = np.vstack((np_white_pieces, np_black_pieces)).tolist()
        
    def display(self):
        print("  x 1 2 3 4 5 6 7 ")
        print("y")
        for row in range(7):
            print(str(row+1) + "   ", end='')
            for column in range(7):
                piece_index = self.getPieceIndexByCoordinates(column+1, row+1)
                if piece_index == -1:
                    print(" ", end='')
                elif piece_index < 6:
                    print("O", end='')
                else:
                    print("X", end='')
                if column+1 != 7: print(',', end='')
            print("")
        print("")
        
    def isValidMove(self, move):
        #check that the move makes sense
        
        if (move.oldCoordinates[0] == move.newCoordinates[0] and move.oldCoordinates[1] == move.newCoordinates[1]) \
            or (move.oldCoordinates[0] != move.newCoordinates[0] and move.oldCoordinates[1] != move.newCoordinates[1]): return False
        if move.oldCoordinates[0] < 1 or move.oldCoordinates[1] < 1 \
            or move.oldCoordinates[0] > 7 or move.oldCoordinates[1] > 7 \
                or move.newCoordinates[0] < 1 or move.newCoordinates[1] < 1 \
                    or move.newCoordinates[0] > 7 or move.newCoordinates[1] > 7: return False
        
        #check that a piece is at oldCoordinates
        piece_index = self.getPieceIndexByCoordinates(move.oldCoordinates[0],move.oldCoordinates[1])
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
    
    def numFreeSquaresInDirection(self, start_coordinates, step_amt):
        i = [start_coordinates[0] + step_amt[0], start_coordinates[1] + step_amt[1]]
        num_steps = 0
        while True:
            if i[0] < 1 or i[1] < 1 or i[0] > 7 or i[1] > 7 or num_steps >= 3 or i in self.pieces:
                return num_steps
            else:
                i[0] += step_amt[0]
                i[1] += step_amt[1]
                num_steps += 1
                
    def numSquaresMovable(self, piece_index):
        if piece_index < 6:
            enemy_pieces = self.pieces[6:]
        else:
            enemy_pieces = self.pieces[:6]
        
        max_move_dist = 3
        for e in enemy_pieces:
            close = (e[0]-self.pieces[piece_index][0])**2 <= 1 and (e[1]-self.pieces[piece_index][1])**2 <= 1
            if close:
                max_move_dist -= 1
                if max_move_dist == 0: break
        return max_move_dist
    
    def update(self, move, check_validity=False):
        if check_validity and not self.isValidMove(move):
            print("Invalid move: " + str(move))
            exit()
        piece_index = self.getPieceIndexByCoordinates(move.oldCoordinates[0],move.oldCoordinates[1])
        self.pieces[piece_index] = move.newCoordinates
        
    def getWinner(self):
        p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11,p12 = self.pieces
        w1 = tuple(p1)
        w2 = tuple(p2)
        w3 = tuple(p3)
        w4 = tuple(p4)
        w5 = tuple(p5)
        w6 = tuple(p6)
        
        # (1, 2, 3, 4) - 1
        # (1, 2, 3, 5) - 2
        # (1, 2, 3, 6) - 3
        # (1, 2, 4, 5) - 4
        # (1, 2, 4, 6) - 5
        # (1, 2, 5, 6) - 6
        # (1, 3, 4, 5) - 7
        # (1, 3, 4, 6) - 8
        # (1, 3, 5, 6) - 9
        # (1, 4, 5, 6) - 10
        # (2, 3, 4, 5) - 11
        # (2, 3, 4, 6) - 12
        # (2, 3, 5, 6) - 13
        # (2, 4, 5, 6) - 14
        # (3, 4, 5, 6) - 15
        if is_square_map[frozenset([w1, w2, w3, w4])] or \
                is_square_map[frozenset([w1, w2, w3, w5])] or \
                is_square_map[frozenset([w1, w2, w3, w6])] or \
                is_square_map[frozenset([w1, w2, w4, w5])] or \
                is_square_map[frozenset([w1, w2, w4, w6])] or \
                is_square_map[frozenset([w1, w2, w5, w6])] or \
                is_square_map[frozenset([w1, w3, w4, w5])] or \
                is_square_map[frozenset([w1, w3, w4, w6])] or \
                is_square_map[frozenset([w1, w3, w5, w6])] or \
                is_square_map[frozenset([w1, w4, w5, w6])] or \
                is_square_map[frozenset([w2, w3, w4, w5])] or \
                is_square_map[frozenset([w2, w3, w4, w6])] or \
                is_square_map[frozenset([w2, w3, w5, w6])] or \
                is_square_map[frozenset([w2, w4, w5, w6])] or \
                is_square_map[frozenset([w3, w4, w5, w6])]: return 0
        
        b1 = tuple(p7)
        b2 = tuple(p8)
        b3 = tuple(p9)
        b4 = tuple(p10)
        b5 = tuple(p11)
        b6 = tuple(p12)
                
        if is_square_map[frozenset([b1, b2, b3, b4])] or \
                is_square_map[frozenset([b1, b2, b3, b5])] or \
                is_square_map[frozenset([b1, b2, b3, b6])] or \
                is_square_map[frozenset([b1, b2, b4, b5])] or \
                is_square_map[frozenset([b1, b2, b4, b6])] or \
                is_square_map[frozenset([b1, b2, b5, b6])] or \
                is_square_map[frozenset([b1, b3, b4, b5])] or \
                is_square_map[frozenset([b1, b3, b4, b6])] or \
                is_square_map[frozenset([b1, b3, b5, b6])] or \
                is_square_map[frozenset([b1, b4, b5, b6])] or \
                is_square_map[frozenset([b2, b3, b4, b5])] or \
                is_square_map[frozenset([b2, b3, b4, b6])] or \
                is_square_map[frozenset([b2, b3, b5, b6])] or \
                is_square_map[frozenset([b2, b4, b5, b6])] or \
                is_square_map[frozenset([b3, b4, b5, b6])]: return 1
        
        return None
        
    def _quality(self, color, depth, winner=-1):
        if winner == -1: winner = self.getWinner()
        
        if winner == color: return 1 # AGENT WIN
        elif winner is not None: return -1 # OPPONENT WIN
        return 0
        
    def quality(self, color, depth, winner=False):
        if winner == False: winner = self.getWinner()
        
        if winner == color: return 100000 - depth # AGENT WIN
        elif winner is not None: return -100000 + depth # OPPONENT WIN
        # OTHERWISE NO CLEAR WINNER
        #good heuristic: distance between pieces and 
        
        i_offset = color*6
        opp_i_offset = 6 - i_offset
        
        score = 0
        for i in indices_to_check:
            our_piece_i_x, our_piece_i_y = self.pieces[i+i_offset]
            opponent_piece_i_x, opponent_piece_i_y = self.pieces[i+opp_i_offset]
            
            for j in indices_to_check:
                opponent_piece_j_x, opponent_piece_j_y = self.pieces[j+opp_i_offset]
                
                distance_between_agent_and_enemy = (our_piece_i_x-opponent_piece_j_x) * (our_piece_i_y-opponent_piece_j_y)
                score += 0.4 * distance_between_agent_and_enemy*distance_between_agent_and_enemy
                if j <= i: continue
                our_piece_j_x, our_piece_j_y = self.pieces[j+i_offset]
                agent_distance_to_self = (our_piece_i_x-our_piece_j_x) * (our_piece_i_y-our_piece_j_y)
                enemy_distance_to_self = (opponent_piece_i_x-opponent_piece_j_x) * (opponent_piece_i_y-opponent_piece_j_y)
                score += (enemy_distance_to_self*enemy_distance_to_self - agent_distance_to_self*agent_distance_to_self)

        return score
    
    def possibleNextStates(self, color):
        i_offset = color*6
        opp_i_offset = 6 - i_offset
        
        p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11,p12 = self.pieces
        
        possible_next_states = []
        for i in indices_to_check:
            movable_piece_x, movable_piece_y = self.pieces[i+i_offset]
            max_move_dist = 3
            for e_i in indices_to_check:
                e = self.pieces[e_i+opp_i_offset]
                close = (e[0]-movable_piece_x)**2 <= 1 and (e[1]-movable_piece_y)**2 <= 1
                if close:
                    max_move_dist -= 1
                    if max_move_dist == 0: break
            if max_move_dist == 0: continue
            move_options = range(max_move_dist)
            for direction in directions:
                pieceCoordinatesAfterMove = [movable_piece_x, movable_piece_y]
                for _ in move_options:
                    pieceCoordinatesAfterMove[0] += direction[0]
                    pieceCoordinatesAfterMove[1] += direction[1]
                    if pieceCoordinatesAfterMove[0] < 1 or pieceCoordinatesAfterMove[1] < 1 \
                        or pieceCoordinatesAfterMove[0] > 7 or pieceCoordinatesAfterMove[1] > 7 \
                            or pieceCoordinatesAfterMove in self.pieces: break
                    
                    possible_state = State(ignoreSetup=True)
                    possible_state.pieces = [[p1[0], p1[1]], \
                                            [p2[0], p2[1]], \
                                            [p3[0], p3[1]], \
                                            [p4[0], p4[1]], \
                                            [p5[0], p5[1]], \
                                            [p6[0], p6[1]], \
                                            [p7[0], p7[1]], \
                                            [p8[0], p8[1]], \
                                            [p9[0], p9[1]], \
                                            [p10[0], p10[1]], \
                                            [p11[0], p11[1]], \
                                            [p12[0], p12[1]]]
                    possible_state.pieces[i+i_offset][0] = pieceCoordinatesAfterMove[0]
                    possible_state.pieces[i+i_offset][1] = pieceCoordinatesAfterMove[1]
                    
                    possible_next_states.append(possible_state)
        
        return possible_next_states
    
    def getPieceIndexByCoordinates(self,x,y):
        try:
            return self.pieces.index([x,y])
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
        else:
            self.oldCoordinates = oldCoordinates
            self.newCoordinates = newCoordinates
        
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
            
        self.oldCoordinates = [piece_to_move_row, piece_to_move_col]
        self.newCoordinates = [piece_new_row, piece_new_col]
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

with open('caching/is_square_map.pickle', 'rb') as file:
    is_square_map = pickle.load(file)

#global variables for performance: no need to instantiate these every time since they are constant
directions = [[-1,0], [1,0], [0,-1], [0,1]]
indices_to_check = range(6)

test_list = [9]*1000