from utils.GameClasses import State, Color
from utils.Agent import Agent

def checkForGameEnd(board_state, colorTurn):
    winner = board_state.getWinner()
    if winner is not None:
        print("Game Over!")
        if winner == Color.white: winner = "White"
        else: winner = "Black"
        print(winner + " wins!")
        exit()
    if len(board_state.possibleNextStates(colorTurn)) == 0:
        print("Stalemate! (" + ("White" if colorTurn == Color.white else "Black") + " cannot move)")
        exit()    

board_state = State()
board_state.display()

white_player = Agent(Color.white, maxSearchDepth=4, fractionalDepth=0.5, fractionDepthLimit=2)
black_player = Agent(Color.black, maxSearchDepth=4, fractionalDepth=0.5, fractionDepthLimit=2)

while True:
    white_move = white_player.getNextMove(board_state)
    print("White plays " + str(white_move))
    board_state.update(white_move, check_validity=True)
    checkForGameEnd(board_state, Color.black)
    board_state.display()
    black_move = black_player.getNextMove(board_state)
    print("Black plays " + str(black_move))
    board_state.update(black_move, check_validity=True)
    checkForGameEnd(board_state, Color.white)
    board_state.display()