from utils.GameClasses import State
from utils.Agent import Agent, GameClient

def checkForGameEnd(board_state, colorTurn):
    winner = board_state.getWinner()
    if winner is not None:
        print("Game Over!")
        print(str("Black" if winner else "White") + " wins!")
        exit()
    if len(board_state.possibleNextStates(colorTurn)) == 0:
        print("Stalemate! (" + str("Black" if colorTurn else "White") + " cannot move)")
        


def q1():
    for depth in [3,4,5,6]:
        print("DEPTH",depth)
        for alpha_beta in [True,False]:
            print("ALPHA BETA:", alpha_beta)
            white_player = Agent(0, minSearchDepth=depth, time_cutoff=100000, iterative_deepening=False, useAlphaBetaPruning=alpha_beta)
            print("SCENARIO A")
            board_state = State(whitePieceCoordinates=[(2,1), (6,2), (1,4), (7,6), (1,7), (2,7)], blackPieceCoordinates=[(5,1), (6,1), (7,1), (5,2), (7,2), (7,7)])
            # board_state.display()
            white_player.getNextMove(board_state)
            print("SCENARIO B")
            board_state = State(whitePieceCoordinates=[(6,1), (6,4), (2,6), (6,6), (3,7), (4,7)], blackPieceCoordinates=[(6,2), (5,3), (6,3), (6,5), (1,7), (2,7)])
            # board_state.display()
            white_player.getNextMove(board_state)
            print("SCENARIO C")
            board_state = State(whitePieceCoordinates=[(6,1), (7,1), (5,2), (6,4), (7,6), (7,7)], blackPieceCoordinates=[(6,2), (7,2), (2,6), (6,6), (2,7), (3,7)])
            # board_state.display()
            white_player.getNextMove(board_state)

def q2():
    for shuffle in [True,False]:
        print("SHUFFLE:", shuffle)
        for alpha_beta in [True,False]:
            for i in range(3):
                print("RUN",i)
                print("ALPHA BETA:", alpha_beta)
                white_player = Agent(0, minSearchDepth=4, time_cutoff=100000, iterative_deepening=False, useAlphaBetaPruning=alpha_beta, shuffle_next_states=shuffle)
                print("SCENARIO A")
                board_state = State(whitePieceCoordinates=[(2,1), (6,2), (1,4), (7,6), (1,7), (2,7)], blackPieceCoordinates=[(5,1), (6,1), (7,1), (5,2), (7,2), (7,7)])
                # board_state.display()
                white_player.getNextMove(board_state)
                print("SCENARIO B")
                board_state = State(whitePieceCoordinates=[(6,1), (6,4), (2,6), (6,6), (3,7), (4,7)], blackPieceCoordinates=[(6,2), (5,3), (6,3), (6,5), (1,7), (2,7)])
                # board_state.display()
                white_player.getNextMove(board_state)
                print("SCENARIO C")
                board_state = State(whitePieceCoordinates=[(6,1), (7,1), (5,2), (6,4), (7,6), (7,7)], blackPieceCoordinates=[(6,2), (7,2), (2,6), (6,6), (2,7), (3,7)])
                # board_state.display()
                white_player.getNextMove(board_state)

def q3():
    for shuffle in [True,False]:
        print("SHUFFLE:", shuffle)
        # for alpha_beta in [False, True]:
        #     print("ALPHA BETA:",alpha_beta)
        def checkForGameEnd(board_state, colorTurn):
            winner = board_state.getWinner()
            if winner is not None:
                print("Game Over!")
                print(str("Black" if winner else "White") + " wins!")
                exit()
            if len(board_state.possibleNextStates(colorTurn)) == 0:
                print("Stalemate! (" + str("Black" if colorTurn else "White") + " cannot move)")
                exit()    

        board_state = State(whitePieceCoordinates=[(6,1), (7,1), (5,2), (6,4), (7,6), (7,7)], blackPieceCoordinates=[(6,2), (7,2), (2,6), (6,6), (2,7), (3,7)])
        # board_state.display()

        white_player = Agent(0, minSearchDepth=6, time_cutoff=100000, iterative_deepening=False, useAlphaBetaPruning=True, shuffle_next_states=shuffle)
        black_player = Agent(1, minSearchDepth=6, time_cutoff=100000, iterative_deepening=False, useAlphaBetaPruning=True, shuffle_next_states=shuffle)

        num_turns_white = 0
        num_turns_black = 0

        for i in range(6):
            white_move = white_player.getNextMove(board_state)
            print("White plays " + str(white_move))
            num_turns_white += 1
            # print("Num turns white:", num_turns_black)
            board_state.update(white_move, check_validity=True)
            # board_state.display()
            checkForGameEnd(board_state, 1)
            black_move = black_player.getNextMove(board_state)
            print("Black plays " + str(black_move))
            num_turns_black += 1
            # print("Num turns black:", num_turns_black)
            board_state.update(black_move, check_validity=True)
            # board_state.display()
            checkForGameEnd(board_state, 0)

def q4():
    for depth in [3,4,5,6]:
        print("DEPTH",depth)
        for alpha_beta in [True,False]:
            print("ALPHA BETA:", alpha_beta)
            white_player = Agent(0, minSearchDepth=depth, time_cutoff=100000, iterative_deepening=False, useAlphaBetaPruning=alpha_beta)
            print("SCENARIO A")
            board_state = State(whitePieceCoordinates=[(2,1), (6,2), (1,4), (7,6), (1,7), (2,7)], blackPieceCoordinates=[(5,1), (6,1), (7,1), (5,2), (7,2), (7,7)])
            # board_state.display()
            white_player.getNextMove(board_state)
            print("SCENARIO B")
            board_state = State(whitePieceCoordinates=[(6,1), (6,4), (2,6), (6,6), (3,7), (4,7)], blackPieceCoordinates=[(6,2), (5,3), (6,3), (6,5), (1,7), (2,7)])
            # board_state.display()
            white_player.getNextMove(board_state)
            print("SCENARIO C")
            board_state = State(whitePieceCoordinates=[(6,1), (7,1), (5,2), (6,4), (7,6), (7,7)], blackPieceCoordinates=[(6,2), (7,2), (2,6), (6,6), (2,7), (3,7)])
            # board_state.display()
            white_player.getNextMove(board_state)
    

# q1()
# q2()
# q3()
q4()


print("DONE!")