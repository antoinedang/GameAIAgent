from gameClasses import State, Move, Color
from agent import Agent, GameClient

def checkForGameEnd(board_state):
    winner = board_state.getWinner()
    if winner is not None:
        print("Game Over!")
        if winner == Color.white: winner = "White"
        elif winner == Color.white: winner = "Black"
        else: winner = "Stalemate. No one"
        print(winner + " wins!")
        exit()

board_state = State()

board_state.display()

white_player = Agent(Color.white)
black_player = Agent(Color.black)

while True:
    white_move = white_player.getNextMove(board_state)
    print("White plays " + str(white_move))
    board_state.update(white_move)
    checkForGameEnd(board_state)
    board_state.display()
    black_move = black_player.getNextMove(board_state)
    print("Black plays " + str(black_move))
    board_state.update(black_move)
    checkForGameEnd(board_state)
    board_state.display()