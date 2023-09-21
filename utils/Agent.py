from utils.GameClasses import State, Move, Color
import math
import socket

class Agent:
    def __init__(self, color, maxSearchDepth=5):
        self.color = color
        self.opponent_color = Color.other(color)
        self.maxSearchDepth = maxSearchDepth
        self.opponent_stalemate = 0.01
        self.agent_stalemate = -0.01
        
    def getNextMove(self, state):
        best_next_state = self.alphaBetaMiniMaxSearch(state)[1]
        if best_next_state is None:
            print("No moves available. Forfeiting.")
            exit()
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
        return bestValue, (bestChildState if depth == 0 else None)

class GameClient:
    def __init__(self, color, gameID, ip="156trlinux-1.ece.mcgill.ca", port=12345, initialBoardState=State()):
        self.board_state = initialBoardState
        print("Starting agent.")
        self.agent = Agent(color)
        self.board_state.display()
        self.gameID = gameID
        self.port = port
        self.ip = ip
        self.color = color
        
    def start(self):
        #TODO connect to server at hostname:port
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.connect((self.ip, self.port))
        print("Successfully connected to game server.")
        server.send("game{} {}\n".format(self.gameID, "white" if self.color == Color.white else "black").encode())
        print("Registered in game ID {} as the {} player.".format(self.gameID, "white" if self.color == Color.white else "black"))
        if self.color == Color.white: #play first
            #compute our move and send to server
            our_move = self.agent.getNextMove(self.board_state)
            server.send(str(our_move).encode())
            
            #update state of the board after the move
            self.board_state.update(our_move)
            self.board_state.display()
            self.checkForGameEnd(Color.other(self.color))
            
        #start game
        while True:
            #receive message from server for opponent move
            opponent_move = server.recv(1024).decode()
            if self.color in opponent_move: continue # ignore messages about our own moves
            print("Received " + opponent_move)
            
            #update state of the board after opponent's move
            self.board_state.update(Move(string=opponent_move), check_validity=True)
            self.board_state.display()
            self.checkForGameEnd(self.color)
            
            #decide our move and send to server
            our_move = self.agent.getNextMove(self.board_state)
            server.send(str(our_move).encode())
            print("Sent " + our_move)
            
            #update state of the board after our move
            self.board_state.update(our_move)
            self.board_state.display()
            self.checkForGameEnd(Color.other(self.color))
        
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