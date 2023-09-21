from utils.GameClasses import State
from utils.Agent import Agent

def checkForGameEnd(board_state, colorTurn):
    winner = board_state.getWinner()
    if winner is not None:
        print("Game Over!")
        print(str(winner) + " wins!")
        exit()
    if len(board_state.possibleNextStates(colorTurn)) == 0:
        print("Stalemate! (" + str(colorTurn) + " cannot move)")
        exit()    

board_state = State()
board_state.display()

white_player = Agent(0, time_cutoff=9)
black_player = Agent(1, time_cutoff=9)

while True:
    white_move = white_player.getNextMove(board_state)
    print("W plays " + str(white_move))
    board_state.update(white_move, check_validity=True)
    board_state.display()
    checkForGameEnd(board_state, 1)
    black_move = black_player.getNextMove(board_state)
    print("B plays " + str(black_move))
    board_state.update(black_move, check_validity=True)
    board_state.display()
    checkForGameEnd(board_state, 0)