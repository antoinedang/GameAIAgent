Part I
Implement a game-playing agent to play the game of Dynamic Connect-4 against a human. Your agent must be capable of playing either white or black. The time limit for the computer (which must be one of the Trotttier Engineering Linux servers, accessible via 156TRLinux.ece.mcgill.ca) to transmit its move to the game server is 10 seconds. Although this is not mandatory, we suggest that you display a simple text-only "visualization" of the game state, both for debugging purposes, but also, for human inspection of the game play sequence.  Such a display should represent the current board state as a matrix of comma-separated characters, with O denoting a white piece, X denoting a black piece, and suitably formatted whitespace denoting an empty square. For example, the starting board configuration above would be represented as follows:

 ,X,X, ,O, ,
 , , , , , ,X
O, , , , , , 
O, , , , , ,O
 , , , , , ,O
X, , , , , , 
 , ,O, ,X,X, 

Each square in the grid can be labeled by its <x,y>position, with <1,1> (corrected) referring to the top-left corner of the board (thus, <2,1> corresponds to the top-left black piece in the initial formation). Plays are communicated to the game sever by specifying the position of the piece to move in the form <x,y>followed by one of the compass directions, N, S, E, W; and the number of squares to move. For example, to move the black piece at the top left of the board one square to the left, the command would be 21W1. Each time it performs a move, your agent should also echo the associated command for human inspection.

For this part of the assignment you may evaluate game states as being either a win (+1), a loss for (-1), or a neutral state (0). Implement both the minimax and alpha-beta algorithms. Also, your program should have an option for specifying the initial game state (either through an input file or manually, as you wish). This will be used to test your program with specific game scenarios.

In your report, consider the three game states shown below:

 ,O, , ,X,X,X
 , , , ,X,O,X
 , , , , , , 
O, , , , , , 
 , , , , , , 
 , , , , , ,O
O,O, , , , ,X
     (a)
 	
 , , , , ,O, 
 , , , , ,X, 
 , , , ,X,X, 
 , , , , ,O, 
 , , , , ,X, 
 ,O, , , ,O, 
X,X,O,O, , , 
     (b)
 	
, , , , ,O,O
 , , , ,O,X,X
 , , , , , , 
 , , , , ,O, 
 , , , , , , 
 ,X, , , ,X,O
 ,X,X, , , ,O
     (c)
     
Indicate the total number of states visited by your program, starting from each state shown, when using depth cutoffs of 3, 4, 5 and 6, both with minimax and alpha-beta. Assume it is white's turn to play.
Does the number of states visited depend on the order in which you generate new states during the search? 1) Explain your answer and 2) justify it using results from your program.
If two agents are to play against each other for scenario (c) for a depth cutoff of 6, for which, if any, of minimax and/or alpha-beta pruning will the losing agent try to delay its defeat? Explain your answer.



Part II
In Part I of this assignment, our evaluation function was extremely simplistic. This left our agent with the ability to make intelligent moves only when its lookahead horizon could detect a sequence leading to a guaranteed win. However, as described in the text, when we are forced to cut off the search at non-leaf nodes, we can exploit a heuristic evaluation function to provide a meaningful value representing the "goodness" of the corresponding state.

Your task is to design a useful heuristic evaluation function for non-terminal nodes and demonstrate that it leads to improved performance (compared to the evaluation function in Part I). Note that in addition to playing "well" when confronted with non-terminal nodes, your agent should also exhibit the following behaviour:

when victory is certain for your agent, it should try to win as soon as possible
when defeat is certain for your agent, it should play so as to delay its defeat as much as possible.
In your report:

Provide a rationale for the choice of the improved evaluation function you used. In particular, explain how you implemented the behaviour described above.
For a given search depth, does your improved evaluation function reduce the average number of nodes visited with 1) minimax? 2) alpha-beta? Illustrate appropriately.
Discuss the computational tradeoffs with the use of a more complex evaluation function with respect to the depth of the game tree that can be evaluated.
For a depth cutoff of 4 for scenarios (a) and (c) in part 1, give a log of the game by two agents that use your developed heuristic. (In other words, run two instances of the code, with each playing one of the sides, and having its moves communicated via the game server, just as will be done in the class tournament).
Game Server
In order to permit coordination with other players for the class tournament and ensure that time constraints of 10 seconds per move are respected, your agent will communicate by TCP with the game server, running on the specified server_hostname and server_port. The instructor is running the "official" game server on 156trlinux-1.ece.mcgill.ca port 12345, which you are free to use for testing during development.

Your submission must compile (or interpret) successfully on the Trottier Engineering Linux machines and run correctly through the game server, both playing white and black, or you will not be eligible to participate in the class tournament. From past experience, please make sure you test this early in your development or you will likely be disappointed.

For human readability, all communications sent to the game server must be terminated by a newline character ('\n'), and similarly, all communications received from the game server will be terminated by a newline character. Referring to the example at the start of the assignment, to move the black piece at the top left of the board one square to the left, the agent would send the string "21W1\n" to the game server.

The first message from any player to the server must specify the gameID and colour, e.g., "game37 white\n". The server automatically matches white and black players using the same gameID. Each (legal) subsequent message sent to the server corresponds to a move and is echoed back to both players. 

The server is responsible for parsing the messages, validating their syntax, and sending back replies to both players. However, it does not retain the state of the game in memory nor validate the moves. That remains your responsibility. Humans can connect to the server with nc, e.g., nc 156trlinux-1.ece.mcgill.ca 12345 to play against an agent program.

For the benefit of diagnostics, the server will return human-readable error messages as appropriate. Failure to transmit a valid move to the DC4Server within the time constraints allowed by the server will result in an automatic loss of the game. Potential draw situations will be assessed by the (human) judge.