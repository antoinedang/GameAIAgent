from utils.GameClasses import State, Move
import math
import socket
import time

class Agent:
    def __init__(self, color, minSearchDepth=3, time_cutoff=9, iterative_deepening=True, useAlphaBetaPruning=True):
        self.color = color
        self.opponent_color = color ^ 1
        self.minSearchDepth = minSearchDepth
        self.time_cutoff = time_cutoff if iterative_deepening else math.inf
        self.opponent_stalemate = 0.01
        self.agent_stalemate = -0.01
        self.next_states = []
        self.iterative_deepening = iterative_deepening
        self.useAlphaBetaPruning = useAlphaBetaPruning
        self.move_threshold_to_seperate = 30
        self.try_to_seperate_pieces = False
        
    def getNextMove(self, state):
        print(len(state.possibleNextStates(self.color) + state.possibleNextStates(self.opponent_color)))
        if len(state.possibleNextStates(self.color) + state.possibleNextStates(self.opponent_color)) < self.move_threshold_to_seperate:
            self.try_to_seperate_pieces = True
        else:
            self.try_to_seperate_pieces = False
        self.start_time = time.time()
        self.extraDepth = 0
        
        best_next_state = self.alphaBetaMiniMaxSearch(state)[1]
        while self.iterative_deepening:
            self.extraDepth += 1
            try:
                best_next_state = self.alphaBetaMiniMaxSearch(state)[1]
            except TimeoutError:
                break
        if best_next_state is None:
            print("No moves available. Forfeiting.")
            exit()
        if not self.iterative_deepening: self.extraDepth += 1
        print(" >> {} searched {} moves ahead.\n".format("Black" if self.color else "White", self.minSearchDepth + self.extraDepth - 1))
        return state.getMoveToState(best_next_state)
    
    def alphaBetaMiniMaxSearch(self, state, depth=0, alpha=-math.inf, beta=math.inf, isMaxPlayerTurn=True):
        if time.time() - self.start_time > self.time_cutoff: raise TimeoutError
        if depth >= self.minSearchDepth + self.extraDepth: return state.quality(self.color, depth, self.try_to_seperate_pieces), None
        winner = state.getWinner()
        if winner is not None: return state.quality(self.color, depth, self.try_to_seperate_pieces, winner=winner), None
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
                if self.useAlphaBetaPruning and alpha >= beta: break
        else:
            bestValue = math.inf
            next_states = state.possibleNextStates(self.opponent_color)
            if len(next_states) == 0: return self.opponent_stalemate, None
            for child_state in next_states:
                value = self.alphaBetaMiniMaxSearch(child_state, depth+1, alpha, beta, True)[0]
                if bestValue > value:
                    bestValue = value
                if bestValue < beta: beta = bestValue
                if self.useAlphaBetaPruning and alpha >= beta: break
        return bestValue, bestChildState

class GameClient:
    def __init__(self, color, gameID, ip="156trlinux-1.ece.mcgill.ca", port=12345, initialBoardState=State()):
        self.board_state = initialBoardState
        print("\nStarting agent...")
        self.agent = Agent(color)
        self.gameID = gameID
        self.port = port
        self.ip = ip
        self.color = color
        
    def start(self):
        #TODO connect to server at hostname:port
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.connect((self.ip, self.port))
        registration_msg = "game{} {}\n".format(self.gameID, "black" if self.color else "white")
        server.send((registration_msg).encode())
        print("\nSuccessfully connected to game server. Starting gameplay.\n")
        opponent_registration_msg = "game{} {}\n".format(self.gameID, "white" if self.color else "black")
        last_move_sent = ""
        
        self.board_state.display()
        
        if not self.color: #play first
            #compute our move and send to server
            our_move = self.agent.getNextMove(self.board_state)
            server.send(str(our_move).encode())
            print("Sent " + str(our_move))
            last_move_sent = str(our_move)
            
            #update state of the board after the move
            self.board_state.update(our_move)
            self.board_state.display()
            self.checkForGameEnd(1)
            
        print("Waiting for opponent move...\n")
        #start game
        while True:
            #receive message from server for opponent move
            received = server.recv(1024).decode()
            move = None
            for msg in received.split('\n'):
                if len(msg) == 0: continue
                msg += '\n'
                if msg == registration_msg: continue
                elif msg == opponent_registration_msg:
                    print("Opponent has joined the game.")
                    continue
                elif msg == last_move_sent:
                    last_move_sent = ""
                    continue
                move = msg
                
            if move is None: continue
            print("Received " + str(move))
            
            #update state of the board after opponent's move
            self.board_state.update(Move(string=move), check_validity=True)
            self.board_state.display()
            self.checkForGameEnd(self.color)
            
            print("Searching for best move...\n")
            #decide our move and send to server
            our_move = self.agent.getNextMove(self.board_state)
            server.send(str(our_move).encode())
            print("Sent " + str(our_move))
            last_move_sent = str(our_move)
            
            #update state of the board after our move
            self.board_state.update(our_move)
            self.board_state.display()
            self.checkForGameEnd(self.color ^ 1)
            print("Waiting for opponent move...\n")
        
    def checkForGameEnd(self, colorTurn):
        winner = self.board_state.getWinner()
        if winner is not None:
            print("Game Over!")
            print(str("Black" if winner else "White") + " wins!")
            exit()
        if len(self.board_state.possibleNextStates(colorTurn)) == 0:
            print("Stalemate! (" + str("Black" if colorTurn else "White") + " cannot move)")