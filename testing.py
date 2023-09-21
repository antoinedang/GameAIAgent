from utils.GameClasses import State, Color, Move
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
white_player = Agent(Color.white)
black_player = Agent(Color.black)


# for i in range(10000):
#     board_state.possibleNextStates(Color.black)
#     board_state.possibleNextStates(Color.white)



for i in range(1):
    white_move = white_player.getNextMove(board_state)
    print("White plays " + str(white_move))
exit()
# board_state.display()
# board_state.update(white_move)
# checkForGameEnd(board_state, Color.black)

# while True:
#     white_move = white_player.getNextMove(board_state)
#     print("White plays " + str(white_move))
#     board_state.update(white_move, check_validity=True)
#     checkForGameEnd(board_state, Color.black)
#     board_state.display()
#     black_move = black_player.getNextMove(board_state)
#     print("Black plays " + str(black_move))
#     board_state.update(black_move, check_validity=True)
#     checkForGameEnd(board_state, Color.white)
#     board_state.display()