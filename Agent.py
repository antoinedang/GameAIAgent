from gameClasses import State, Move, Color
import math

class Agent:
    def __init__(self, color, maxSearchDepth=10):
        self.color = color
        self.maxSearchDepth = maxSearchDepth
    def getNextMove(self, state):
        return state.getMoveToState(self.alphaBetaMiniMaxSearch(state)[1])
    def alphaBetaMiniMaxSearch(self, state, depth=0, alpha=-math.inf, beta=math.inf, isMaxPlayerTurn=True):
        if depth > self.maxSearchDepth or state.getWinner() is not None: return state.quality(self.color), state
        if isMaxPlayerTurn:
            bestValue = -math.inf, None
            for state in state.possibleNextStates():
                value = self.alphaBetaMiniMaxSearch(child_state, depth+1, alpha, beta, False)
                bestValue = max(bestValue, value, key=lambda x: x[0])
                alpha = max(alpha, bestValue[0])
                if alpha >= beta: break
        else:
            bestValue = math.inf, None       
            for child_state in state.possibleNextStates():
                value = self.alphaBetaMiniMaxSearch(child_state, depth+1, alpha, beta, True)
                bestValue = min(bestValue, value, key=lambda x: x[0])
                beta = min(alpha, bestValue[0])
                if alpha >= beta: break
        return bestValue

class GameClient:
    def __init__(self, hostname, port, color, gameID, initialBoardState=State()):
        self.board_state = initialBoardState
        print("Starting gameplay.")
        agent = Agent(color)
        self.board_state.display()
        #TODO connect to server at hostname:port
        
        server.send("game{} {}\n".format(gameID, "white" if color == Color.white else "black"))
        
        if color == Color.white: #play first
            #compute our move and send to server
            our_move = agent.getNextMove(self.board_state)
            server.send(str(our_move))
            
            #update state of the board after the move
            self.board_state.update(our_move)
            self.board_state.display()
            self.checkForGameEnd()
            
        #start game
        while True:
            #receive message from server for opponent move
            opponent_move = server.receive()
            if color in opponent_move: continue # ignore messages about our own moves
            print("Received " + opponent_move)
            
            #update state of the board after opponent's move
            self.board_state.update(Move(string=opponent_move))
            self.board_state.display()
            self.checkForGameEnd()
            
            #decide our move and send to server
            our_move = agent.getNextMove(self.board_state)
            server.send(str(our_move))
            print("Sent " + our_move)
            
            #update state of the board after our move
            self.board_state.update(our_move)
            self.board_state.display()
            self.checkForGameEnd()
        
    def checkForGameEnd(self):
        winner = self.board_state.getWinner()
        if winner is not None:
            print("Game Over!")
            if winner == Color.white: winner = "White"
            else: winner = "Black"
            print(winner + " wins!")
            exit()