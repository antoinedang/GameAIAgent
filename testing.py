from utils.GameClasses import State, Move
from utils.Agent import Agent

def checkForGameEnd(board_state, colorTurn):
    winner = board_state.getWinner()
    if winner is not None:
        print("Game Over!")
        print(str(winner) + " wins!")
        exit()
    if len(board_state.possibleNextStates(colorTurn)) == 0:
        print("Stalemate! (" + str(colorTurn) + " cannot move)")
        

board_state = State()
board_state.display()
# board_state.update(Move(string="34N1\n"))
# board_state.display()
# print(board_state.getWinner())
# exit()
white_player = Agent(0, iterative_deepening=False, minSearchDepth=5)
black_player = Agent(1)


# for i in range(50000):
#     board_state.possibleNextStates(1)
#     board_state.possibleNextStates(0)



for i in range(1):
    white_move = white_player.getNextMove(board_state)
    print("White plays " + str(white_move))
exit()
# board_state.display()
# board_state.update(white_move)
# checkForGameEnd(board_state, 1)

# while True:
#     white_move = white_player.getNextMove(board_state)
#     print("White plays " + str(white_move))
#     board_state.update(white_move, check_validity=True)
#     checkForGameEnd(board_state, 1)
#     board_state.display()
#     black_move = black_player.getNextMove(board_state)
#     print("Black plays " + str(black_move))
#     board_state.update(black_move, check_validity=True)
#     checkForGameEnd(board_state, 0)
#     board_state.display()