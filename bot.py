from stockfish import Stockfish
import chess
import chess.engine
import subprocess
import sys
import math
import os


board = chess.Board()


exePath = os.getcwd() + "/stockfish/stockfish-windows-x86-64-universal.exe"


class Player(): #Player is a base class wrapper, so the game loop can function without different problems per mode.

    def __init__(self, name, side):
            self.name = name
            self.side = side
    
    def makeDecision(self, board):
        pass
    

class HumanPlayer(Player) :
    def makeDecision(self, board):
        playerInput = input("Enter your move: ")

        return playerInput

class StockFishPlayer(Player) : 
     def makeDecision(self, board):
        result = engine.play(board, chess.engine.Limit(time = 1.0))
        
        return result.move.uci()




pieceValues = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 20000
}
#for Black -> if used for white, set to negative.
#early game tables

Piece_SquareEG_PAWN = [ #taken off Gemini for position weights.
    0,  0,  0,  0,  0,  0,  0,  0,
    50, 50, 50, 50, 50, 50, 50, 50,
    10, 10, 20, 30, 30, 20, 10, 10,
    5,  5, 10, 25, 25, 10,  5,  5,
    0,  0,  0, 20, 20,  0,  0,  0,
    5, -5,-10,  0,  0,-10, -5,  5,
    5, 10, 10,-20,-20, 10, 10,  5,
    0,  0,  0,  0,  0,  0,  0,  0
]
Piece_SquareEG_KNIGHT = [
    -50,-40,-30,-30,-30,-30,-40,-50e2
    -40,-20,  0,  0,  0,  0,-20,-40,
    -30,  0, 10, 15, 15, 10,  0,-30,
    -30,  5, 15, 20, 20, 15,  5,-30,
    -30,  0, 15, 20, 20, 15,  0,-30,
    -30,  5, 10, 15, 15, 10,  5,-30,
    -40,-20,  0,  5,  5,  0,-20,-40,
    -50,-40,-30,-30,-30,-30,-40,-50
]
Piece_SquareEG_KING = [
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -20, -30, -30, -40, -40, -30, -30, -20,
    -10, -20, -20, -20, -20, -20, -20, -10,
     20,  20,   0,   0,   0,   0,  20,  20,
     20,  30,  10,   0,   0,  10,  30,  20
]
Piece_SquareEG_BISHOP = [
    -20, -10, -10, -10, -10, -10, -10, -20,
    -10,   0,   0,   0,   0,   0,   0, -10,
    -10,   0,   5,  10,  10,   5,   0, -10,
    -10,   5,   5,  10,  10,   5,   5, -10,
    -10,   0,  10,  10,  10,  10,   0, -10,
    -10,  10,  10,  10,  10,  10,  10, -10,
    -10,   5,   0,   0,   0,   0,   5, -10,
    -20, -10, -10, -10, -10, -10, -10, -20
]
Piece_SquareEG_ROOK = [
    0,   0,   0,   0,   0,   0,   0,   0,
    5,  10,  10,  10,  10,  10,  10,   5,
    -5,   0,   0,   0,   0,   0,   0,  -5,
    -5,   0,   0,   0,   0,   0,   0,  -5,
    -5,   0,   0,   0,   0,   0,   0,  -5,
    -5,   0,   0,   0,   0,   0,   0,  -5,
    -5,   0,   0,   0,   0,   0,   0,  -5,
    0,   0,   0,   5,   5,   0,   0,   0
]
Piece_SquareEG_QUEEN = [
    -20,  -10,  -10,   -5,   -5,  -10,  -10,  -20,
    -10,    0,    0,    0,    0,    0,    0,  -10,
    -10,    0,    5,    5,    5,    5,    0,  -10,
    -5,    0,    5,    5,    5,    5,    0,   -5,
    0,    0,    5,    5,    5,    5,    0,   -5,
    -10,    5,    5,    5,    5,    5,    0,  -10,
    -10,    0,    5,    0,    0,    0,    0,  -10,
    -20,  -10,  -10,   -5,   -5,  -10,  -10,  -20
    
]

def returnEGPieceSquare(pieceName):
    if (pieceName == chess.PAWN):
        return Piece_SquareEG_PAWN
    if (pieceName == chess.ROOK):
        return Piece_SquareEG_ROOK
    if (pieceName == chess.KNIGHT):
        return Piece_SquareEG_KNIGHT
    if (pieceName == chess.BISHOP):
        return Piece_SquareEG_BISHOP
    if (pieceName == chess.KING):
        return Piece_SquareEG_KING
    if (pieceName == chess.QUEEN):
        return Piece_SquareEG_QUEEN
    

Piece_SquareLG_PAWN = [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    60,
    60,
    60,
    60,
    60,
    60,
    60,
    60,
    35,
    35,
    35,
    35,
    35,
    35,
    35,
    35,
    20,
    20,
    20,
    20,
    20,
    20,
    20,
    20,
    10,
    10,
    10,
    10,
    10,
    10,
    10,
    10,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
]
Piece_SquareLG_KNIGHT = [
    -40,
    -30,
    -20,
    -20,
    -20,
    -20,
    -30,
    -40,
    -30,
    -10,
    0,
    0,
    0,
    0,
    -10,
    -30,
    -20,
    0,
    15,
    20,
    20,
    15,
    0,
    -20,
    -20,
    5,
    20,
    25,
    25,
    20,
    5,
    -20,
    -20,
    5,
    20,
    25,
    25,
    20,
    5,
    -20,
    -20,
    0,
    15,
    20,
    20,
    15,
    0,
    -20,
    -30,
    -10,
    0,
    0,
    0,
    0,
    -10,
    -30,
    -40,
    -30,
    -20,
    -20,
    -20,
    -20,
    -30,
    -40,
]
Piece_SquareLG_BISHOP = [
    -20,
    -10,
    -10,
    -10,
    -10,
    -10,
    -10,
    -20,
    -10,
    0,
    0,
    0,
    0,
    0,
    0,
    -10,
    -10,
    0,
    10,
    15,
    15,
    10,
    0,
    -10,
    -10,
    5,
    15,
    20,
    20,
    15,
    5,
    -10,
    -10,
    5,
    15,
    20,
    20,
    15,
    5,
    -10,
    -10,
    0,
    10,
    15,
    15,
    10,
    0,
    -10,
    -10,
    0,
    0,
    0,
    0,
    0,
    0,
    -10,
    -20,
    -10,
    -10,
    -10,
    -10,
    -10,
    -10,
    -20,
]
Piece_SquareLG_ROOK = [
    10,
    10,
    10,
    10,
    10,
    10,
    10,
    10,
    25,
    25,
    25,
    25,
    25,
    25,
    25,
    25,
    5,
    5,
    5,
    5,
    5,
    5,
    5,
    5,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    5,
    5,
    0,
    0,
    0,
]
Piece_SquareLG_QUEEN = [
    -15,
    -10,
    -10,
    -5,
    -5,
    -10,
    -10,
    -15,
    -10,
    0,
    5,
    5,
    5,
    5,
    0,
    -10,
    -10,
    5,
    15,
    15,
    15,
    15,
    5,
    -10,
    -5,
    5,
    15,
    20,
    20,
    15,
    5,
    -5,
    -5,
    5,
    15,
    20,
    20,
    15,
    5,
    -5,
    -10,
    5,
    15,
    15,
    15,
    15,
    5,
    -10,
    -10,
    0,
    5,
    5,
    5,
    5,
    0,
    -10,
    -15,
    -10,
    -10,
    -5,
    -5,
    -10,
    -10,
    -15,
]
Piece_SquareLG_KING = [
    -50,
    -40,
    -30,
    -20,
    -20,
    -30,
    -40,
    -50,
    -30,
    -20,
    -10,
    0,
    0,
    -10,
    -20,
    -30,
    -30,
    -10,
    20,
    30,
    30,
    20,
    -10,
    -30,
    -30,
    -10,
    30,
    45,
    45,
    30,
    -10,
    -30,
    -30,
    -10,
    30,
    45,
    45,
    30,
    -10,
    -30,
    -30,
    -10,
    20,
    30,
    30,
    20,
    -10,
    -30,
    -30,
    -20,
    -10,
    0,
    0,
    -10,
    -20,
    -30,
    -50,
    -40,
    -30,
    -20,
    -20,
    -30,
    -40,
    -50,
]
def returnLGPieceSquare(pieceName):
    if (pieceName == chess.PAWN):
        return Piece_SquareLG_PAWN
    if (pieceName == chess.ROOK):
        return Piece_SquareLG_ROOK
    if (pieceName == chess.KNIGHT):
        return Piece_SquareLG_KNIGHT
    if (pieceName == chess.BISHOP):
        return Piece_SquareLG_BISHOP
    if (pieceName == chess.KING):
        return Piece_SquareLG_KING
    if (pieceName == chess.QUEEN):
        return Piece_SquareLG_QUEEN
    
    
def gameProgressionFloat(board): #returns game progression based on material/(allMaterial)
    total_pieces = len(board.piece_map())
    return 1-(total_pieces/32.0)

def lerp(a,b,t):
    return a + (b-a)*t

#needs specific positional evalutation

def evaluateBoard(board): #this does not care what side you are on, it provides an overall scoring method.

    #positional values
    if board.is_checkmate():
        return 99999 if board.turn == chess.WHITE else -99999 #white is minimzing, black is maximizing.
    if board.is_stalemate() or board.is_insufficient_material():
        return 0

    value = 0

    #bishop number penalty
    

    for square, piece in board.piece_map().items():
        pieceValue = pieceValues[piece.piece_type]

        #get the value from the pieceSquare for the piece.
        
        pieceSquareEG = returnEGPieceSquare(piece.piece_type)
        pieceSquareLG = returnLGPieceSquare(piece.piece_type)
        
        positionValue = -pieceSquareEG[chess.square_mirror(square)]
        positionValueLG = -pieceSquareLG[chess.square_mirror(square)]

        positionValue = lerp(positionValue, positionValueLG, gameProgressionFloat(board))

        
        if piece.color == chess.WHITE:
            value -= pieceValue - positionValue     
        else:
            value += pieceValue + positionValue

   
    
    return value


def minimax(board, depth, alpha, beta, maximizingPlayer):
    if depth == 0 or board.is_game_over(): #return the evaluation.
        #evaluate the board, on a scale from -1 to 1, probably.
        value = evaluateBoard(board)

        return value
    elif maximizingPlayer: #this is the mazimizing player, always wants the biggest evaluation.
        value = -math.inf #big negative number, to be overwritten gradually.
            #run every possible move from here
            #update value, take the max of (value, minimax(childNode, depth-1, FALSE))
        for move in board.legal_moves:
            newBoard = board.copy()
            newBoard.push(move)
            eval = minimax(newBoard, depth-1, alpha, beta, False)
            value = max(value, eval)
            alpha = max(alpha,eval)
            newBoard.pop()
            if (beta <= alpha):
                break
        return value
    else: #minimizing player, wants the smallest number.
        value = math.inf # big positive number, to be overwritten gradually.
        #run every possible move from here.
        #update the value, min(value, minimax(childNode, depth − 1, TRUE))
        for move in board.legal_moves:
            newBoard = board.copy()
            newBoard.push(move)
            eval = minimax(newBoard, depth-1, alpha, beta, True)
            value = min(value, eval)
            beta = min(beta, eval)
            newBoard.pop() 
            if (beta <= alpha):
                break
        return value

class VacuousPlayer(Player) : 
    def makeDecision(self,board):
        input = ""

        #run minimax algorithm

        #loop through every legal move that you can do.
        
        bestMove = None
        bestMoveValue = 10000000

        StartPoint = True #start with minimizing, or start with maximizing.
        if (board.turn == chess.WHITE): #if it's white, try to minimize
            StartPoint = False
            bestMoveValue = math.inf
        else:
            StartPoint = True #if it's black, try to maximize.
            bestMoveValue = -math.inf

        for move in board.legal_moves:
            workingBoard = board.copy()
            workingBoard.push(move) 
            value = minimax(workingBoard, 2, -math.inf, math.inf, not StartPoint) 
            if (value < bestMoveValue and board.turn == chess.WHITE):
                bestMoveValue = value
                bestMove = move.uci()
            elif (value > bestMoveValue and board.turn == chess.BLACK):
                bestMoveValue = value
                bestMove = move.uci()
        
        
        return bestMove


#game structure

gameloop = True
increment = 0

whitePlayer = None # = HumanPlayer("human", "white")
blackPlayer = None #= StockFishPlayer("sf", "black")

stockFishInUse = False

def selectMode ():

    global whitePlayer, blackPlayer, stockFishInUse

    invalidChoice = True
    gamemode = input ("Select a gamemode: 1: Player vs Player       2: Player vs Bot      3: Player vs Stockfish       4: Bot vs Stockfish: ")
    while (invalidChoice):
        if gamemode != "1" and gamemode !="2" and gamemode !="3" and gamemode != "4":
            gamemode = input ("Invalid choice, pick a number from 1-4: ")
        else:
            invalidChoice = False
    
    invalidChoice = False

    choiceSide = input("Select a colour for first player, white or black: ")

    choiceSide = choiceSide.lower().strip()
   
    invalidSide = True
    while(invalidSide):
        if choiceSide == "white" or choiceSide == "black":
            print("You have selected a side for player")
            invalidSide = False 
        else:
            choiceSide = (input("Select a colour for first player, white or black: ")
            .strip()
            .lower()
            )

    
    match gamemode:
        case "1":  # PvP
            if choiceSide == "white":
                whitePlayer = HumanPlayer("Human 1", "white")
                blackPlayer = HumanPlayer("Human 2", "black")
            else:
                whitePlayer = HumanPlayer("Human 2", "white")
                blackPlayer = HumanPlayer("Human 1", "black")

        case "2":  # Player vs Vacuous Bot
            if choiceSide == "white":
                whitePlayer = HumanPlayer("Human", "white")
                blackPlayer = VacuousPlayer("Bot", "black")
            else:
                whitePlayer = VacuousPlayer("Bot", "white")
                blackPlayer = HumanPlayer("Human", "black")

        case "3":  # Player vs Stockfish
            stockFishInUse = True
            if choiceSide == "white":
                whitePlayer = HumanPlayer("Human", "white")
                blackPlayer = StockFishPlayer("Stockfish", "black")
                stockFishInUse = True
            else:
                whitePlayer = StockFishPlayer("Stockfish", "white")
                blackPlayer = HumanPlayer("Human", "black")
                stockFishInUse = True

        case "4":  # Vacuous Bot vs Stockfish
            stockFishInUse = True
            if choiceSide == "white":
                whitePlayer = VacuousPlayer("Bot", "white")
                blackPlayer = StockFishPlayer("Stockfish", "black")
                stockFishInUse = True
            else:
                whitePlayer = StockFishPlayer("Stockfish", "white")
                blackPlayer = VacuousPlayer("Bot", "black")
                stockFishInUse = True

selectMode()

engine = None
if (stockFishInUse):
    engine = chess.engine.SimpleEngine.popen_uci(exePath)
    #do not active the engine if not necessary.


#gameloop is everything that runs during a ply. 

while (gameloop):
    
    print("-"*20) 

    #print the board.
    print(board.unicode(borders=True, orientation=board.turn))

    #get the player Object
    turnPlayer = whitePlayer if board.turn == chess.WHITE else blackPlayer

    #gets the player's move. (see each implementation for details)
    moveInput = turnPlayer.makeDecision(board)
    
    if moveInput.lower() == 'quit':
        print("game over")
        gameloop = False

    try:
        move = board.parse_san(moveInput) if moveInput in [board.san(m) for m in board.legal_moves] else board.parse_uci(moveInput)
        #check if the move is legal
        if move in board.legal_moves:
            board.push(move)  # Make the move on the board
        else:
            print("Illegal move! Try again.")
                
    except ValueError:
        print("Invalid input format! Use e.g. 'e4' or 'e2e4'.")
        
    print("\n")
    
    gameloop = not board.is_game_over()

print("--- GAME OVER ---")
print(board)
print(f"Reason: {board.outcome().termination.name.replace('_', ' ').title()}")

if board.is_checkmate():
    # The player whose turn it WAS when checkmate happened is the loser
    winner = "Black" if board.turn == chess.WHITE else "White"
    print(f"Checkmate {winner} wins!")
else:
    print("Draw game.")

if (stockFishInUse):
    engine.quit()

sys.exit(0)

