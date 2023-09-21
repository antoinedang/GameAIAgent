from utils.GameClasses import State, Move, Color
from utils.Agent import Agent, GameClient

def checkForGameEnd(board_state, colorTurn):
    winner = board_state.getWinner()
    if winner is not None:
        print("Game Over!")
        print(str(winner) + " wins!")
        exit()
    if len(board_state.possibleNextStates(colorTurn)) == 0:
        print("Stalemate! (" + str(colorTurn) + " cannot move)")
        



for depth in [3,4,5]:
    white_player = Agent(Color.white)
    
    board_state = State(whitePieceCoordinates=[(2,1), (6,2), (1,4), (7,6), (1,7), (2,7)], blackPieceCoordinates=[(5,1), (6,1), (7,1), (5,2), (7,2), (7,7)])
    board_state.display()
    white_move = white_player.getNextMove(board_state)
    print("White plays " + str(white_move))

    board_state = State(whitePieceCoordinates=[(7,1), (7,4), (2,6), (7,6), (3,7), (4,7)], blackPieceCoordinates=[(7,2), (6,3), (7,3), (7,5), (1,7), (2,7)])
    board_state.display()
    white_move = white_player.getNextMove(board_state)
    print("White plays " + str(white_move))

    board_state = State(whitePieceCoordinates=[(6,1), (7,1), (5,2), (6,4), (7,6), (7,7)], blackPieceCoordinates=[(6,2), (7,2), (2,6), (6,6), (2,7), (3,7)])
    board_state.display()
    white_move = white_player.getNextMove(board_state)
    print("White plays " + str(white_move))