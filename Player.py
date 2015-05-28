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
import timeit

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
    
    def __init__(self, playerNum, playerType, ply=0):    
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
            at a given board configuation"""
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
        """combin three function to evalue current status"""

        if self.num == 1:
            Cups = board.P1Cups
            oppCups = board.P2Cups
        else:
            Cups = board.P2Cups
            oppCups = board.P1Cups
    
        s1 =0.0
        s2 =0.0
        #my cups remain stones, 0 cups has average value
        for i in range(len(Cups)):
            s1=s1 + Cups[i]
            #print "S1=" + str(s1)+" cup:"+str(i) +" value:"+str(Cups[i])
        s1= s1*1.0
        #my Mancula stones
        s1 = s1+board.scoreCups[self.num-1]*5.0
        #opp cups
        for i in range(len(oppCups)):
            s2 = s2 + oppCups[i]
        
        s2 = s2 *1.0
        #opp Mancala
        s2 = s2+board.scoreCups[self.opp-1]*5.0
        
        #print "S1=" +str(s1) +" S2="+str(s2)


        if board.scoreCups[self.num-1] >= 25:
            return s1 - s2 + 100.0
        elif board.scoreCups[self.opp-1] >= 25:
            return s1 - s2 - 100.0
        else:
            return s1 - s2
    def score_TTT(self, board):
    
        if board.hasWon( self.num ):
            return 100.0
        elif board.hasWon( self.opp ):
            return 0.0
        else:
            return 50.0
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
        score = -INFINITY
        turn = self
        alpha = -INFINITY
        beta = INFINITY
        #print "alphaBetaMove init"+" Ply="+str(ply)
        #print board.legalMoves( self )
        score, move = self.maxValueAB(board, ply, turn, alpha, beta)
        #print "alphaBetaMove finish score="+str(score)+" move="+str(move)+" Ply="+str(ply)
        return score, move
        
    def maxValueAB( self, board, ply, turn, a, b):
        """ Find the minimax value for the next move for this player
            at a given board configuation
            Returns (score, oppMove)"""
        alpha = a
        beta = b
        if board.gameOver():
            return (turn.score( board ), -1)
        score = -INFINITY
        move = -1
        #print "Max into ply="+str(ply)+"status num="+str(len(board.legalMoves( self )))+" Ply="+str(ply)
        #print "----------Max---------------- Ply="+str(ply)
        #print board.legalMoves( self )
        #print "---------end Max------------- Ply="+str(ply)
        movelist =board.legalMoves( self )
        for m in movelist:
            if ply == 0:
                #print "Max Return ply="+str(ply)+" score ="+str(turn.score( board ))+" Move="+str(m)+" Ply="+str(ply)
                return (turn.score( board ), m)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            again = nextBoard.makeMove( self, m )
            #print "Max Call Min ply:"+str(ply)+" alpha="+str(alpha)+" beta:"+str(beta)+" Move"+str(m)+" Ply="+str(ply)
            #if it is my turn again then FIXME HERE
            if again:
                #print "Max move agian score >= Beta! Score:"+str(score)+" beta="+str(beta)+" move:"+str(move)+" Ply="+str(ply)
                s, oppMove= self.maxValueAB(nextBoard, ply-1, turn, alpha , beta)
            else:
                s, oppMove= opponent.minValueAB(nextBoard, ply-1, turn, alpha , beta)
            #print "Max return score:"+str(s)+" beta="+str(beta)+" move:"+str(m)+" Ply="+str(ply)
            if s > score:
                move = m
                score = s
        
            #pruning other moves
            if score >= beta:
                #print "Max Pruing score >= Beta! Score:"+str(score)+" beta="+str(beta)+" move:"+str(move)+" Ply="+str(ply)
                #print board.legalMoves( self )
                #print "Max Pruing end------------------------"
                return (score, move)
            #update a and b value
            if score > alpha:
                #print "Max update Alpha old="+str(alpha)+" new="+str(score)+" Ply="+str(ply)
                alpha = score

        return (score, move)
    
    def minValueAB( self, board, ply, turn, a, b):
        """ Find the minimax value for the next move for this player
            at a given board configuation"""
        alpha = a
        beta = b
        if board.gameOver():
            return (turn.score( board ), -1)
        score = INFINITY
        move = -1
        #print "Min into ply="+str(ply)+"status num="+str(len(board.legalMoves( self )))+" Ply="+str(ply)
        #print "----------Min---------------- Ply="+str(ply)
        #print board.legalMoves( self )
        #print "---------end Min------------- Ply="+str(ply)
        for m in board.legalMoves( self ):
            if ply == 0:
                #print "Min Return ply="+str(ply)+" score ="+str(turn.score( board ))+" Move="+str(m)+" Ply="+str(ply)
                return (turn.score( board ), m)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            again = nextBoard.makeMove( self, m )
            #print "Min Call Max ply:"+str(ply)+" alpha="+str(alpha)+" beta:"+str(beta)+" Move"+str(m)+" Ply="+str(ply)
            #if it is my turn again then FIXME HERE
            if again :
                #print "Min move agian score >= Beta! Score:"+str(score)+" beta="+str(beta)+" move:"+str(move)+" Ply="+str(ply)
                s, oppMove = self.minValueAB(nextBoard, ply-1, turn, alpha, beta)
            else:
                s, oppMove = opponent.maxValueAB(nextBoard, ply-1, turn, alpha, beta)
            #print "Min return score:"+str(s)+"beta="+str(beta)+"move:"+str(m)
            if s < score:
                score = s
                move = m
            
            #pruning other moves
            if score <= alpha:
                #print "Min Pruing score <= Alpha score:"+str(score)+" alpha="+str(alpha)+"move:"+str(m)+" Ply="+str(ply)
                #print board.legalMoves( self )
                #print "Min Pruing end------------------------"
                return (score, move)
            #update a and b value
            if score < beta:
                #print "Min update Beta old="+str(beta)+"new="+str(score)+" Ply="+str(ply)
                beta = score
        
        return (score, move)

                
    def chooseMove( self, board ):
        """ Returns the next move that this player wants to make """
        start = timeit.default_timer()
        

        if self.type == self.HUMAN:
            move = input("Please enter your move:")
            while not board.legalMove(self, move):
                print move, "is not valid"
                move = input( "Please enter your move" )
            stop = timeit.default_timer()
            print "Use Time:"+str(stop - start) +"Seconds"
            return move
        elif self.type == self.RANDOM:
            move = choice(board.legalMoves(self))
            #print "RANDOM chose move", move, "with value", val
            stop = timeit.default_timer()
            print "Use Time:"+str(stop - start) +"Seconds"
            return move
        elif self.type == self.MINIMAX:
            val, move = self.minimaxMove( board, self.ply )
            print "MINIMAX chose move", move, " with value", val
            stop = timeit.default_timer()
            print "Use Time:"+str(stop - start) +"Seconds"
            return move
        elif self.type == self.ABPRUNE:
            val, move = self.alphaBetaMove( board, self.ply)
            print "ABPRUNE chose move", move, " with value", val
            stop = timeit.default_timer()
            print "Use Time:"+str(stop - start) +"Seconds"
            return move
        elif self.type == self.CUSTOM:
            # TODO: Implement a custom player
            # You should fill this in with a call to your best move choosing
            # function.  You may use whatever search algorithm and scoring
            # algorithm you like.  Remember that your player must make
            # each move in about 10 seconds or less.
            val, move = self.alphaBetaMove( board, 10)
            
            #print "CUSTOM chose move", move, " with value", val
            stop = timeit.default_timer()
            print "Use Time:"+str(stop - start) +"Seconds"
            return move
        else:
            print "Unknown player type"
            stop = timeit.default_timer()
            print "Use Time:"+str(stop - start) +"Seconds"
            return -1

    def score1(self, board):

        if self.num == 1:
            Cups = board.P1Cups
            oppCups = board.P2Cups
        else:
            Cups = board.P2Cups
            oppCups = board.P1Cups
        
        s1 =0.0
        s2 =0.0
        #my cups remain stones, 0 cups has average value
        
        for i in range(len(Cups)):
            s1=s1 + ((Cups[i]*Cups[i]/2)* (0.8+i*0.05))
            #land in empty pit
            if Cups[i]+i <= 5:
                if Cups[Cups[i]+i]== 0:
                    s1 = s1 +oppCups[5-Cups[i]-i]*5.5
            #if next move is in Mancala
            if Cups[i]+i == 6:
                s1 = s1 + 20

        #print "S1=" + str(s1)+" cup:"+str(i) +" value:"+str(Cups[i])
        #my Mancula stones
        s1 = s1+board.scoreCups[self.num-1]*5.5
        #opp cups
        
        for i in range(len(oppCups)):
            s2 = s2 + oppCups[i]*1.0

        #opp Mancala
        s2 = s2+board.scoreCups[self.opp-1]*5.0
    
        #print "S1=" +str(s1) +" S2="+str(s2)
    
    
        if board.scoreCups[self.num-1] >= 24:
            return s1 - s2 + 100.0
        elif board.scoreCups[self.opp-1] >= 24:
            return s1 - s2 - 100.0
        else:
            return s1 - s2


# Note, you should change the name of this player to be a custom name
# that identifies you or your team.
class Xin(Player):
    """ Defines a player that knows how to evaluate a Mancala gameboard
        intelligently """

    def score(self, board):
        """ Evaluate the Mancala board for this player """
        # Currently this function just calls Player's score
        # function.  You should replace the line below with your own code
        # for evaluating the board
        #print "MancalaGuru score"
        if self.num == 1:
            Cups = board.P1Cups
            oppCups = board.P2Cups
        else:
            Cups = board.P2Cups
            oppCups = board.P1Cups
        
        s1 =0.0
        s2 =0.0
        #my cups remain stones, 0 cups has average value

    
        #print "S1=" + str(s1)+" cup:"+str(i) +" value:"+str(Cups[i])
        #my Mancula stones
        s1 = s1+board.scoreCups[self.num-1]*5.5
        #opp cups
        
        #opp Mancala
        s2 = s2+board.scoreCups[self.opp-1]*5.0
        
        #print "S1=" +str(s1) +" S2="+str(s2)
        
        
        if board.scoreCups[self.num-1] >= 24:
            return s1 - s2 + 100.0
        elif board.scoreCups[self.opp-1] >= 24:
            return s1 - s2 - 100.0
        else:
            return s1 - s2
    def chooseMove( self, board ):
        start = timeit.default_timer()
        val, move = self.alphaBetaMove( board, 10)
        print "Xin ABPRUNE chose move", move, " with value", val
        stop = timeit.default_timer()
        print "Use Time:"+str(stop - start) +"Seconds"
        return move

       




