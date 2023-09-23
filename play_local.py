from utils.GameClasses import State
from utils.Agent import Agent

def checkForGameEnd(board_state, colorTurn):
    winner = board_state.getWinner()
    if winner is not None:
        print("Game Over!")
        print(str("Black" if winner else "White") + " wins!")
        exit()
    if len(board_state.possibleNextStates(colorTurn)) == 0:
        print("Stalemate! (" + str("Black" if colorTurn else "White") + " cannot move)")
        exit()    

board_state = State()
# board_state = State(whitePieceCoordinates=[(2,1), (6,2), (1,4), (7,6), (1,7), (2,7)], blackPieceCoordinates=[(5,1), (6,1), (7,1), (5,2), (7,2), (7,7)])
# board_state = State(whitePieceCoordinates=[(6,1), (7,1), (5,2), (6,4), (7,6), (7,7)], blackPieceCoordinates=[(6,2), (7,2), (2,6), (6,6), (2,7), (3,7)])

board_state.display()

white_player = Agent(0, time_cutoff=9)
black_player = Agent(1, time_cutoff=9)

while True:
    white_move = white_player.getNextMove(board_state)
    print("White plays " + str(white_move))
    board_state.update(white_move, check_validity=True)
    board_state.display()
    checkForGameEnd(board_state, 1)
    black_move = black_player.getNextMove(board_state)
    print("Black plays " + str(black_move))
    board_state.update(black_move, check_validity=True)
    board_state.display()
    checkForGameEnd(board_state, 0)