from GameClasses import State, Move, Color

class Agent:
    def __init__(self, color):
        self.color = color
    def getBestMove(state):
    def nextStates(state):
    def quality(State state):
    def isEndState(State state):
        
        
    
class GameClient:
    def __init__(self, hostname, port, color, gameID, initialState):
        self.playing = True
        board_state = initialState
        agent = Agent(color)
        self.display(board_state)
        #TODO connect to server at hostname:port
        
        if color == Color.white: #play first
            #compute first move
            our_move = agent.getBestMove(board_state)
            #send move to server
            server.send(self.encodeMove(our_move))
            #update state of the board after the move
            board_state.update(our_move)
            #display the state of the board after the move
            self.display(board_state)
            
        #start game
        while self.playing:
            #receive message from server for opponent move
            opponent_move = server.receive()
            if color in opponent_move: continue # ignore messages about our own moves
            #update state of the board after opponent's move
            board_state.update(self.decodeMove(opponent_move))
            self.display(board_state)
            our_move = agent.getBestMove(board_state)
            board_state.update(self.decodeMove(msg_rcv))
            self.display(board_state)
            server.send()
            msg_rcv = server.receive()
            
    def display(self, board_state):
        print("")
    def 
    def decodeMove(self,string):
        return move
    def encodeMove(self,move):
        return ""