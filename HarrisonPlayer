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
    
    def __init__(self, playerNum, playerType, ply=5):    
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
                return (self.score(board, board), m)
            if board.gameOver():
                return (-1, -1)  # Can't make a move, the game is over
            nb = deepcopy(board)
            again = nb.makeMove(self, m)
            if again:
                return again, m
            opp = Player(self.opp, self.type, self.ply)
            s, oppMove = opp.minValue(nb, board, ply-1, turn)
            if s > score:
                move = m
                score = s
        return score, move

    def maxValue( self, board, orgBoard, ply, turn):
        """ Find the minimax value for the next move for this player
            at a given board configuation
            Returns (score, oppMove)"""
        if board.gameOver():
            return (turn.score( board, orgBoard ), -1)
        score = -INFINITY
        move = -1
        for m in board.legalMoves( self ):
            if ply == 0:
                return (turn.score( board, orgBoard ), m)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove( self, m )
            s, oppMove = opponent.minValue(nextBoard, orgBoard, ply-1, turn)
            if s > score:
                move = m
                score = s
        return (score, move)
    
    def minValue( self, board, orgBoard, ply, turn ):
        """ Find the minimax value for the next move for this player
            at a given board configuation"""
        if board.gameOver():
            return turn.score( board, orgBoard ), -1
        score = INFINITY
        move = -1
        for m in board.legalMoves( self ):
            if ply == 0:
                return (turn.score( board, orgBoard ), m)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove( self, m )
            s, oppMove = opponent.maxValue(nextBoard, orgBoard, ply-1, turn)
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
        for m in board.legalMoves( self ):
            if ply == 0:
                return (self.score(board, board), m)
            if board.gameOver():
                return (-1, -1)  # Can't make a move, the game is over
            nb = deepcopy(board)
            again = nb.makeMove(self, m)
            if again:
                return again, m
            opp = Player(self.opp, self.type, self.ply)
            tempA, tempB = opp.minValueAB(nb, board, ply-1, turn, a, b)
            if tempB > a:
                move = m
                a = tempB
        return a, move
        
    def maxValueAB( self, board, orgBoard, ply, turn, a, b):
        """ Find the minimax value for the next move for this player
            at a given board configuation
            Returns (score, oppMove)"""
        if board.gameOver():
            return (turn.score( board, orgBoard ), b)
        score = INFINITY
        move = -1
        for m in board.legalMoves( self ):
            if ply == 0:
                return (turn.score( board, orgBoard ), b)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            if (a < b):
                nextBoard.makeMove( self, m )
                tempA, tempB = opponent.minValueAB(nextBoard, orgBoard, ply-1, turn, a, b)
                if tempB > a:
                    a = tempB
                    move = m
        return (a, b)
    
    def minValueAB( self, board, orgBoard, ply, turn, a, b):
        """ Find the minimax value for the next move for this player
            at a given board configuation"""
        if board.gameOver():
            return (a, turn.score( board, orgBoard ))
        score = INFINITY
        move = -1
        for m in board.legalMoves( self ):
            if ply == 0:
                return (a, turn.score( board, orgBoard ))
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            if (a < b):
                nextBoard.makeMove( self, m )
                tempA, tempB = opponent.maxValueAB(nextBoard, orgBoard, ply-1, turn, a, b)
                if tempA < b:
                    b = tempA
                    move = m
        return (a, b)

                
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
            val, move = self.minimaxMove( board, self.ply )
            print "chose move", move, " with value", val
            return move
        elif self.type == self.ABPRUNE:
            val, move = self.alphaBetaMove( board, self.ply)
            print "chose move", move, " with value", val
            return move
        elif self.type == self.CUSTOM:
            val, move = self.alphaBetaMove( board, self.ply)
            print "chose move", move, " with value", val
            return move
        else:
            print "Unknown player type"
            return -1


# Note, you should change the name of this player to be a custom name
# that identifies you or your team.
class HarrisonPlayer(Player):
    """ Defines a player that knows how to evaluate a Mancala gameboard
        intelligently """

    def score(self, board, orgBoard):
        """ Evaluate the Mancala board for this player """
        if self.num == 2:
            player = 1
            opp = 0
        else:
            opp = 1
            player = 0
        if board.scoreCups[opp] > 24:
            return -1000
        elif board.scoreCups[player] > 24:
            return 1000
        else:
            score = 0
            score+=(board.scoreCups[player]-orgBoard.scoreCups[player])*10
            score-=(board.scoreCups[opp]-orgBoard.scoreCups[opp])*10
        return score


       




