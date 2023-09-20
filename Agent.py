from gameClasses import State, Move, Color
import math

class Agent:
    def __init__(self, color, maxSearchDepth=5):
        self.color = color
        self.opponent_color = Color.other(color)
        self.maxSearchDepth = maxSearchDepth
        self.opponent_stalemate = 0.01
        self.agent_stalemate = -0.01
        
    def getNextMove(self, state):
        best_next_state = self.alphaBetaMiniMaxSearch(state)[1]
        return state.getMoveToState(best_next_state)
    
    def alphaBetaMiniMaxSearch(self, state, depth=0, alpha=-math.inf, beta=math.inf, isMaxPlayerTurn=True):
        if depth >= self.maxSearchDepth: return state.quality(self.color, depth), None
        winner = state.getWinner()
        if winner is not None: return state.quality(self.color, depth, winner=winner), None
        bestChildState = None     
        if isMaxPlayerTurn:
            bestValue = -math.inf
            next_states = state.possibleNextStates(self.color)
            if len(next_states) == 0: return self.agent_stalemate, None
            for child_state in next_states:
                value = self.alphaBetaMiniMaxSearch(child_state, depth+1, alpha, beta, False)[0]
                if bestValue < value:
                    bestValue = value
                    bestChildState = child_state
                if bestValue > alpha: alpha = bestValue
                if alpha >= beta: break
        else:
            bestValue = math.inf
            next_states = state.possibleNextStates(self.opponent_color)
            if len(next_states) == 0: return self.opponent_stalemate, None
            for child_state in next_states:
                value = self.alphaBetaMiniMaxSearch(child_state, depth+1, alpha, beta, True)[0]
                if bestValue > value:
                    bestValue = value
                if bestValue < beta: beta = bestValue
                if alpha >= beta: break
        return bestValue, bestChildState

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
            self.board_state.update(Move(string=opponent_move), check_validity=True)
            self.board_state.display()
            self.checkForGameEnd(color)
            
            #decide our move and send to server
            our_move = agent.getNextMove(self.board_state)
            server.send(str(our_move))
            print("Sent " + our_move)
            
            #update state of the board after our move
            self.board_state.update(our_move)
            self.board_state.display()
            self.checkForGameEnd(Color.other(color))
        
    def checkForGameEnd(self, colorTurn):
        winner = self.board_state.getWinner()
        if winner is not None:
            print("Game Over!")
            if winner == Color.white: winner = "White"
            else: winner = "Black"
            print(winner + " wins!")
            exit()
        if len(self.board_state.possibleNextStates(colorTurn)) == 0:
            print("Stalemate! (" + ("White" if colorTurn == Color.white else "Black") + " cannot move)")