# File: Player.py
# Author: 
# Date: 
# Defines a simple artificially intelligent player agent
# You will define the alpha-beta pruning search algorithm
# You will also define the score function in the MancalaPlayer class,
# a subclass of the Player class.


from random import *
from decimal import *
from copy import *
from MancalaBoard import *

# a constant
INFINITY = 1.0e400

def max(a, b):
    if a>=b:
        return a
    return b
def min(a, b):
    if a<=b:
        return a
    return b

class Player:
    """ A basic AI (or human) player """
    HUMAN = 0
    RANDOM = 1
    MINIMAX = 2
    ABPRUNE = 3
    CUSTOM = 4
    
    def __init__(self, playerNum, playerType, ply=6):    
        self.num = playerNum
        self.opp = 2 - playerNum + 1
        self.type = playerType
        self.ply = ply

    def __repr__(self):
        return str(self.num)
        
    def minimaxMove( self, board, ply ):
        """ Choose the best minimax move.  Returns (move, val) """
        move = -1
        score = -INFINITY
        turn = self
        for m in board.legalMoves( self ):
            if ply == 0:
                return (self.score(board), m)
            if board.gameOver():
                return (-1, -1)  # Can't make a move, the game is over
            nb = deepcopy(board)
            nb.makeMove(self, m)
            opp = Player(self.opp, self.type, self.ply)
            s, oppMove = opp.minValue(nb, ply-1, turn)
            if s > score:
                move = m
                score = s
        return score, move

    def maxValue( self, board, ply, turn):
        """ Find the minimax value for the next move for this player
            at a given board configuation
            Returns (score, oppMove)"""
        if board.gameOver():
            return (turn.score( board ), -1)
        score = -INFINITY
        move = -1
        for m in board.legalMoves( self ):
            if ply == 0:
                return (turn.score( board ), m)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove( self, m )
            s, oppMove = opponent.minValue(nextBoard, ply-1, turn)
            if s > score:
                move = m
                score = s
        return (score, move)
    
    def minValue( self, board, ply, turn ):
        """ Find the minimax value for the next move for this player
            at a given board configuration"""
        if board.gameOver():
            return turn.score( board ), -1
        score = INFINITY
        move = -1
        for m in board.legalMoves( self ):
            if ply == 0:
                return (turn.score( board ), m)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove( self, m )
            s, oppMove = opponent.maxValue(nextBoard, ply-1, turn)
            if s < score:
                score = s
                move = m
        return (score, move)


    # The default player defines a very simple score function
    # You will write the score function in the MancalaPlayer below
    # to improve on this function.
    def score(self, board):
        """ Returns the score for this player given the state of the board """
        if board.hasWon( self.num ):
            return 10000
        elif board.hasWon( self.opp ):
            return -10000
        else:
            if self.num ==1:
                myCups = board.P1Cups
                oppCups = board.P2Cups
            else:
                myCups = board.P2Cups
                oppCups = board.P1Cups
            
            #if someone has more than half the stones game is essentially over
            if board.scoreCups[self.num-1] >24:
                return 10000
            if board.scoreCups[(self.opp-1)] >24:
                return -10000
            
            #set point counter
            points = 0
            
            #5 points for each stone in own mancala. -5 points for opponent
            points += 5 * (board.scoreCups[self.num-1]-board.scoreCups[self.opp-1])
            #5 points for each cup that will grant an extra turn
            
            for x in range (0,6):
                if myCups[x]-(6-x) == 0:
                    points+=5
            for x in range (0,6):
                if oppCups[x] - (6-x) == 0:
                    points-=5
            #3 points for each cup that will score w/o extra turn
            for x in range (0,6):
                if myCups[x]-(6-x) > 0:
                    points+=3
            for x in range (0,6):
                if oppCups[x] - (6-x) > 0:
                    points-=3
            #points for empty cups. Empty close to own mancala is good while empty away is bad
            for x in range (0,6):
                if myCups[x]== 0:
                    points+=(4-(6-x))>>1
            for x in range (0,6):
                if oppCups[x] - (6-x) > 0:
                    points-=(4-(6-x))>>1
            #1 point for total stones left on your side of board
            for x in range (0,6):
                points+=myCups[x]
            for x in range (0,6):
                points-=oppCups[x]
            
            return points

    # You should not modify anything before this point.
    # The code you will add to this file appears below this line.
        
    
    # You will write this function (and any helpers you need)
    # You should write the function here in its simplest form:
    #   1. Use ply to determine when to stop (when ply == 0)
    #   2. Search the moves in the order they are returned from the board's
    #       legalMoves function.
    # However, for your custom player, you may copy this function
    # and modify it so that it uses a different termination condition
    # and/or a different move search order.
    def alphaBetaMove( self, board, ply ):
        """ Choose a move with alpha beta pruning """
        move = -1
        turn = self
        i=1
        a = -INFINITY
        b = INFINITY
        for m in board.legalMoves(self):
            if ply == 0:
                return(self.score(board), m,self.score(board),self.score(board))
            if board.gameOver():
                return(-1,-1)
            nb = deepcopy(board)
            nb.makeMove(self,m)
            opp = Player(self.opp, self.type, self.ply)
            s, oppMove, alpha, beta = opp.minValueAB( nb,(ply-1),turn,a,b)
            if i==1:
                score = s
                i =0
            if score >= beta:
                continue
            else:   
                if a < beta:
                    a = beta
                    score = s
                    move = m 
            print "m: ", m, " score: ", s, "alpha: ", alpha, "beta: ", beta    
            if s == INFINITY: print "s is infinity"               
        return score, move
        
    def maxValueAB( self, board, ply, turn, a, b):           
        if board.gameOver():
            return (turn.score( board ), -1, a, b)        
        move = -1
        i = 1
        for m in board.legalMoves(self):
            if ply == 0:
                return(turn.score(board), m,turn.score(board),turn.score(board))
            nb = deepcopy(board)
            nb.makeMove(self,m)
            opp = Player(self.opp, self.type, self.ply)
            s, oppMove, alpha, beta = opp.minValueAB( nb,ply-1,turn,a,b)
            if i == 1:
                score = s
                i = 0
            if beta> b:
                #if lower branch beta is greater than upper branch beta: prune
                return(s, move, alpha, beta)
            if s> score:
                score = s
                a = s
        return (score, move, a, a)
    
    def minValueAB( self, board, ply, turn, a, b): 
        if board.gameOver():
            return (turn.score( board ), -1, a, b)
        move = -1
        i = 1
        for m in board.legalMoves(self):
            if ply == 0:
                temp = turn.score(board)
                return(temp, m,temp,temp)
            nb = deepcopy(board)
            nb.makeMove(self,m)
            opp = Player(self.opp, self.type, self.ply)
            s, oppMove, alpha, beta = opp.maxValueAB(nb,ply-1,turn,a,b)
            if i == 1: 
                score = s
                b=s
                i = 0
            if alpha < a:
                #if lower branch alpha is less than upper branch alpha:prune
                return (s, move, alpha, beta)
            if s < score:
                score=s
                b=s  
        return (score, move, b, b)

                
    def chooseMove( self, board ):
        """ Returns the next move that this player wants to make """
        if self.type == self.HUMAN:
            move = input("Please enter your move:")
            while not board.legalMove(self, move):
                print move, "is not valid"
                move = input( "Please enter your move" )
            return move
        
        elif self.type == self.RANDOM:
            move = choice(board.legalMoves(self))
            print "chose move", move, "with value", self.score(self,board)
            return move
        elif self.type == self.MINIMAX:
            val, move = self.minimaxMove( board, self.ply )
            print "chose move", move, " with value", val
            return move
        elif self.type == self.ABPRUNE:
            val, move = self.alphaBetaMove( board, self.ply)
            print "chose move", move, " with value", val
            return move
        elif self.type == self.CUSTOM:
            # TODO: Implement a custom player
            # You should fill this in with a call to your best move choosing
            # function.  You may use whatever search algorithm and scoring
            # algorithm you like.  Remember that your player must make
            # each move in about 10 seconds or less.
            
            if self.num ==1:
                myCups = board.P1Cups
                oppCups = board.P2Cups
            else:
                myCups = board.P2Cups
                oppCups = board.P1Cups
            x=-1
            for m in board.legalMoves(self):
                if myCups[m-1]-(7-m) == 0:
                    x = m
            if x >=0:
                val = self.score(board)
                move = x
            else:
                val, move = self.alphaBetaMove1(board, 8)
            print "chose move", move, " with value", val
            return move
        else:
            print "Unknown player type"
            return -1


# Note, you should change the name of this player to be a custom name
# that identifies you or your team.
class Stuart(Player):
    """ Defines a player that knows how to evaluate a Mancala gameboard
        intelligently """
    def __init__(self, playerNum,type):    
        self.num = playerNum
        self.opp = 2 - playerNum + 1
        self.type = type
    def score(self, board):
        """ Evaluate the Mancala board for this player """
        # Currently this function just calls Player's score
        # function.  You should replace the line below with your own code
        # for evaluating the board
        if board.hasWon( self.num ):
            return 10000
        elif board.hasWon( self.opp ):
            return -10000
        else:
            if self.num ==1:
                myCups = board.P1Cups
                oppCups = board.P2Cups
            else:
                myCups = board.P2Cups
                oppCups = board.P1Cups
            
            #if someone has more than half the stones game is essentially over
            if board.scoreCups[self.num-1] >24:
                return 100000
            if board.scoreCups[(self.opp-1)] >24:
                return -100000
            
            #set point counter
            points = 0
            #10 points for each stone in own mancala. -10 points for opponent
            points += 200 *board.scoreCups[self.num-1]-20*board.scoreCups[self.opp-1]
            #10 points for each cup that will grant an extra turn
            for x in range (0,6):
                if myCups[x]-(6-x) == 0:
                    points+=200
            for x in range (0,6):
                if oppCups[x] - (6-x) == 0:
                    points-=20
            #1 points for each cup that will score w/o extra turn
            for x in range (0,6):
                if myCups[x]-(6-x) > 0:
                    points+=1
            for x in range (0,6):
                if oppCups[x] - (6-x) > 0:
                    points-=1
            #points for empty cups. Empty close to own mancala is good while empty away is bad
            for x in range (0,4):
                if myCups[x]== 0:
                    points+=(4+(6-x))
            for x in range (0,4):
                if oppCups[x] == 0:
                    points-=(4+(6-x))
            #1 point for total stones left on your side of board
            for x in range (0,6):
                points+=(myCups[x])
            for x in range (0,6):
                points-=oppCups[x]
            return points

    def alphaBetaMove1( self, board, ply ):
        """ Choose a move with alpha beta pruning """
        move = -1
        turn = self
        i=1
        a = -INFINITY
        b = INFINITY
        for m in board.legalMoves(self):         
            if ply == 0:
                return(self.score(board), m,self.score(board),self.score(board))
            if board.gameOver():
                return(-1,-1)
            nb = deepcopy(board)
            nb.makeMove(self,m)
            opp = Stuart(self.opp, self.type)
            s, oppMove, alpha, beta = opp.minValueAB1( nb,(ply-1),turn,a,b)
            if i==1:
                score = s
                move = m
                i =0
            if score >= beta:
                continue
            else:   
                if a < beta:
                    a = beta
                    score = s
                    move = m 
                              
        return score, move
        
    def maxValueAB1( self, board, ply, turn, a, b):         
        if board.gameOver():
            return (turn.score( board ), -1, a, b)        
        move = -1
        i = 1
        for m in board.legalMoves(self):
            if ply == 0:
                return(turn.score(board), m,turn.score(board),turn.score(board))
            nb = deepcopy(board)
            nb.makeMove(self,m)
            opp = Stuart(self.opp, self.type)
            s, oppMove, alpha, beta = opp.minValueAB1( nb,ply-1,turn,a,b)
            if i == 1:
                score = s
                i = 0
            if beta> b:
                #if lower branch beta is greater than upper branch beta: prune
                return(s, move, alpha, beta)
            if s> score:
                score = s
                a = s
        
        return (score, move, a, a)
    
    def minValueAB1( self, board, ply, turn, a, b):    
        if board.gameOver():
            return (turn.score( board ), -1, a, b)
        move = -1
        i = 1
        for m in board.legalMoves(self):
            if ply == 0:
                temp = turn.score(board)               
                return(temp, m,temp,temp)
            nb = deepcopy(board)
            nb.makeMove(self,m)
            opp = Stuart(self.opp, self.type)
            s, oppMove, alpha, beta = opp.maxValueAB1(nb,ply-1,turn,a,b)
            if i == 1: 
                score = s
                b=s
                i = 0
            if alpha < a:
                #if lower branch alpha is less than upper branch alpha:prune
                return (s, move, alpha, beta)
            if s < score:
                score=s
                b=s  
        return (score, move, b, b)

     
       




