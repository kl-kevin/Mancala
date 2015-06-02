# File: Player.py
# Author: 
# Date: 
# Defines a simple artificially intelligent player agent
# You will define the alpha-beta pruning search algorithm
# You will also define the score function in the MancalaPlayer class,
# a subclass of the Player class.


from random import *
from time import clock
from time import time
from decimal import *
from copy import *
from MancalaBoard import *

# a constant
INFINITY = 1.0e400
PLY = 8

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
    
    def __init__(self, playerNum, playerType, ply=PLY):
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
        score, move, a, b = self.maxValueAB(board, ply, turn, -INFINITY, INFINITY)
        return score, move
        
    def maxValueAB( self, board, ply, turn, a, b):
        """ Find the minimax value for the next move for this player
            at a given board configuation
            Returns (score, oppMove)"""
        if board.gameOver():
            a = max(turn.score( board ), a)
            #print "game over returning ", turn.score( board )
            return (turn.score( board ), -1, a, b)
        score = -INFINITY
        move = -1
        for m in board.legalMoves( self ):
            if ply == 0:
                return (turn.score( board ), m, a, b)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove( self, m )
            s, oppMove, tempA, tempB = opponent.minValueAB(nextBoard, ply-1, turn, a, b)
            if s > score:
                score = s
                move = m
            a = max(score, a)
            if (b <= a):
                #print "alpha is", a, " beta is ", b, "score is ", score, ". Aborted on move", m, "in maxValue"
                return (score, move, a, b)
        return (score, move, a, b)
    
    def minValueAB( self, board, ply, turn, a, b):
        """ Find the minimax value for the next move for this player
            at a given board configuation"""
        if board.gameOver():
            b = min(turn.score( board ), b)
            return (turn.score( board ), -1, a, b)
        score = INFINITY
        move = -1
        for m in board.legalMoves( self ):
            if ply == 0:
                return (turn.score( board ), m, a, b)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove( self, m )
            s, oppMove, tempA, tempB = opponent.maxValueAB(nextBoard, ply-1, turn, a, b)
            if s < score:
                score = s
                move = m
            b = min(score, b)
            if (b <= a):
                #print "alpha is", a, " beta is ", b, "score is ", score, ". Aborted on move", m, "in minValue"
                return (score, move, a, b)
        return (score, move, a, b)

        
    def customMove( self, board, ply ):
        """ Choose a move with alpha beta pruning """
        move = -1
        score = -INFINITY
        turn = self
        score, move, a, b = self.maxValueCustom(board, ply, turn, -INFINITY, INFINITY)
        return score, move
        
    def maxValueCustom( self, board, ply, turn, a, b):
        """ Find the minimax value for the next move for this player
            at a given board configuation
            Returns (score, oppMove)"""
        if board.gameOver():
            a = max(turn.score( board ), a)
            #print "game over returning ", turn.score( board )
            return (turn.score( board ), -1, a, b)
        score = -INFINITY
        move = -1
        moves = board.legalMoves( self )
        shuffle(moves)
        for m in moves:
            if ply == 0:
                return (turn.score( board ), m, a, b)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            moveAgain = nextBoard.makeMove( self, m )
            if (moveAgain):
                s, oppMove, tempA, tempB = self.maxValueCustom(nextBoard, ply-1, turn, a, b)
            else:
                s, oppMove, tempA, tempB = opponent.minValueCustom(nextBoard, ply-1, turn, a, b)
            if s > score:
                score = s
                move = m
            a = max(score, a)
            if (b <= a):
                #print "alpha is", a, " beta is ", b, "score is ", score, ". Aborted on move", m, "in maxValue"
                return (score, move, a, b)
        return (score, move, a, b)
    
    def minValueCustom( self, board, ply, turn, a, b):
        """ Find the minimax value for the next move for this player
            at a given board configuation"""
        if board.gameOver():
            b = min(turn.score( board ), b)
            return (turn.score( board ), -1, a, b)
        score = INFINITY
        move = -1
        moves = board.legalMoves( self )
        shuffle(moves)
        for m in moves:
            if ply == 0:
                return (turn.score( board ), m, a, b)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            moveAgain = nextBoard.makeMove( self, m )
            if (moveAgain):
                s, oppMove, tempA, tempB = self.minValueCustom(nextBoard, ply-1, turn, a, b)
            else:
                s, oppMove, tempA, tempB = opponent.maxValueCustom(nextBoard, ply-1, turn, a, b)
            if s < score:
                score = s
                move = m
            b = min(score, b)
            if (b <= a):
                #print "alpha is", a, " beta is ", b, "score is ", score, ". Aborted on move", m, "in minValue"
                return (score, move, a, b)
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
            print "chose move", move, "with value", val
            return move
        elif self.type == self.MINIMAX:
            #stime = time()
            val, move = self.minimaxMove( board, self.ply )
            #print "elapsed time ", time()-stime
            print "chose move", move, " with value", val
            return move
        elif self.type == self.ABPRUNE:
            #stime = time()
            val, move = self.alphaBetaMove( board, self.ply)
            #print "elapsed time ", time()-stime
            print "chose move", move, " with value", val
            return move
        elif self.type == self.CUSTOM:
            # TODO: Implement a custom player
            # You should fill this in with a call to your best move choosing
            # function.  You may use whatever search algorithm and scoring
            # algorithm you like.  Remember that your player must make
            # each move in about 10 seconds or less.
            stime = time()
            val, move = self.customMove( board, self.ply)
            delta_time = time()-stime
            if (val == 100.0 or val == 0.0):
                self.ply = PLY
            elif (delta_time < 7):
                #print "increasing ply to ", self.ply+1
                self.ply = self.ply+1
            elif (delta_time > 12):
                #print "decreasing ply to ", self.ply-1
                self.ply = self.ply-1
            #print "elapsed time ", delta_time
            print "chose move", move, " with value", val
            return move
        else:
            print "Unknown player type"
            return -1


# Note, you should change the name of this player to be a custom name
# that identifies you or your team.
class AWPMancalaGuru(Player):
    """ Defines a player that knows how to evaluate a Mancala gameboard
        intelligently """

    def score(self, board):
        """ Evaluate the Mancala board for this player """
        # Currently this function just calls Player's score
        # function.  You should replace the line below with your own code
        # for evaluating the board
        if board.hasWon( self.num ):
            return 100.0
        elif board.hasWon( self.opp ):
            return 0.0
        else:
            return 50.0 + board.scoreCups[self.num-1]

       




