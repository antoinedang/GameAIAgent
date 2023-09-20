import pickle
from itertools import combinations

#USE CACHING INSTEAD??
def _formsSquare(pieces):
    min_x = 100
    max_x = -100
    min_y = 100
    max_y = -100
    for piece in pieces:
        x,y = piece
        if x > max_x: max_x = x
        if x < min_x: min_x = x
        if y > max_y: max_y = y
        if y < min_y: min_y = y
    
    return (max_x - min_x) == 1 and (max_y - min_y) == 1

coordinate_options = []
is_square_map = {}

for x in range(8):
    for y in range(8):
        coordinate_options.append((x+1, y+1))
        
for piece_combination in combinations(coordinate_options, 4):
    is_square_map[frozenset(piece_combination)] = _formsSquare(piece_combination)

with open("is_square_map.pickle", "wb") as file:
    pickle.dump(is_square_map, file)