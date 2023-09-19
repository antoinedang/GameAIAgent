from gameClasses import State, Move, Color
from agent import Agent, GameClient

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
        

board_state = State()
board_state.display()

white_player = Agent(Color.white)
black_player = Agent(Color.black)

white_move = white_player.getNextMove(board_state)
# print("White plays " + str(white_move))
# board_state.update(white_move)
# checkForGameEnd(board_state, Color.black)

exit()

for i in range(10):
    white_move = white_player.getNextMove(board_state)
    print("White plays " + str(white_move))
    board_state.update(white_move)
    checkForGameEnd(board_state, Color.black)
    board_state.display()
    black_move = black_player.getNextMove(board_state)
    print("Black plays " + str(black_move))
    board_state.update(black_move)
    checkForGameEnd(board_state, Color.white)
    board_state.display()