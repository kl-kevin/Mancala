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
        a = -INFINITY
        b = INFINITY
        for m in board.legalMoves(self):
            if ply == 0:
                return (self.score(board), m)
            if board.gameOver():
                return (-1, -1)
            if score <= b:
                nb = deepcopy(board)
                nb.makeMove(self, m)
                opp = Player(self.opp, self.type, self.ply)
                s, oppMove, a, b = opp.minValueAB(nb, ply-1, turn, a, b)
                if s > score:
                    move = m
                    score = s
            else:
                #print "beta is ",b,", score is ",score,". Aborted on move ",move," in maxValueAB" 
                break
        return score, move
        
    def maxValueAB( self, board, ply, turn, a, b):
        """ Find the minimax value for the next move for this player
            at a given board configuation
            Returns (score, oppMove)"""
        if board.gameOver():
            #a = turn.score( board )
            #print "game over returning ", turn.score( board )
            return (turn.score( board ), -1, a , b)
        score = -INFINITY
        move = -1
        for m in board.legalMoves( self ):
            if ply == 0:
                return (turn.score( board ), m, a, b)
            if score <= b:
                nb = deepcopy(board)
                nb.makeMove(self, m)
                opp = Player(self.opp, self.type, self.ply)
                s, oppMove, a, b = opp.minValueAB(nb, ply-1, turn, a, b)
                if s > score:
                    move = m
                    score = s
                    a = s
            else:
                break
        #print "alpha is ", a, ", score is ", score, ". Aborted on move ", move, " in maxValueAB on" 
        return (score, move, a, b)
    
    def minValueAB( self, board, ply, turn, a, b):
        """ Find the minimax value for the next move for this player
            at a given board configuation"""
        if board.gameOver():
            return turn.score( board ), -1, a, b
        score = INFINITY
        move = -1
        for m in board.legalMoves( self ):
            if ply == 0:
                return (turn.score( board ), m, a, b)
            if score >= a:
                nb = deepcopy(board)
                nb.makeMove(self, m)
                opp = Player(self.opp, self.type, self.ply)
                s, oppMove, a, b = opp.maxValueAB(nb, ply-1, turn, a, b)
                if s < score:
                    score = s
                    move = m
                    b = s
            else:
                break
        #print "beta is ", a, ", score is ", score, ". Aborted on move ", move, " in minValueAB on"
        return (score, move, a, b)

                
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
            print "RANDOM player chose move", move, "with value", val
            return move
        elif self.type == self.MINIMAX:
            val, move = self.minimaxMove( board, self.ply )
            print "MINIMAX player chose move", move, " with value", val
            return move
        elif self.type == self.ABPRUNE:
            val, move = self.alphaBetaMove( board, self.ply)
            print "ABPRUNE player chose move", move, " with value", val
            return move
        elif self.type == self.CUSTOM:
            # TODO: Implement a custom player
            # You should fill this in with a call to your best move choosing
            # function.  You may use whatever search algorithm and scoring
            # algorithm you like.  Remember that your player must make
            # each move in about 10 seconds or less.
            val, move = self.alphaBetaMove( board, self.ply)
            print "CUSTOM player chose move", move, " with value", val
            return move
        else:
            print "Unknown player type"
            return -1


# Note, you should change the name of this player to be a custom name
# that identifies you or your team.
class KevinPlayer(Player):
    """ Defines a player that knows how to evaluate a Mancala gameboard
        intelligently """

    def __init__(self, playerNum, playerType, ply=5):    
        self.num = playerNum
        self.opp = 2 - playerNum + 1
        self.type = playerType
        self.ply = ply

    def score(self, board):
        """ Evaluate the Mancala board for this player """
        # Currently this function just calls Player's score
        # function.  You should replace the line below with your own code
        # for evaluating the board
        MyCups = board.getPlayersCups(self.num)
        OppCups = board.getPlayersCups(self.opp)
        bonus = 0
        if board.hasWon( self.num ):
            return 100.0
        elif board.hasWon( self.opp ):
            return 0.0
        else:
            for m in range(len(MyCups)):
                if(MyCups[m] + m == 6): #ends in Mancala
                    bonus += 10
                else:
                    spot = MyCups[m] - (6-m) - 6 - 1
                    if (spot >= 0 and spot < 6) and MyCups[spot] == 0 and OppCups[6-m-1] > 0:
                        bonus += 20
                        break
            MyStones = 0
            OppStones = 0
            MyEmptyCups = 0
            OppEmptyCups = 0
            for i in range(len(MyCups)):
                if MyCups[i] == 0:
                    MyEmptyCups += 1
                else:
                    MyStones += MyCups[i]
            for i in range(len(OppCups)):
                if OppCups[i] == 0:
                    OppEmptyCups += 1
                else:
                    OppStones += OppCups[i]
            if MyStones > OppStones:
                bonus += 10
            if MyEmptyCups < OppEmptyCups:
                bonus += 10
            return 10 + bonus

       




