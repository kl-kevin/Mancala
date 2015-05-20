# File: MTCS_Player.py
# Author: Richar Zhang (Zhang, Xin)
# Date: 2015-5-11
# Defines a simple artificially intelligent player agent
# a subclass of the Player class.

from math import *
from decimal import *
from copy import *
from threading import *
from MancalaBoard import *
from Player import *
import random

#class SimulateThread(threading.Thread):
#    def __init__(self,board,event):
#        super(SimulateThread, self).__init__()
#        self.board=board
#        self.event=event

#    def run(self):
        #run the simulate process while (1) untile event comes then end
        #update the tree by call update in the tree(need the lock)

class MTCSPlayer(Player):
    def __init__(self, playerNum, playerType, time =10, ply=1):
        self.num = playerNum
        self.opp = 2 - playerNum + 1
        self.type = playerType
        self.time = time;#seconds for simulation
        self.ply = ply
    
    def __repr__(self):
        return str(self.num)
    


    def chooseMove( self, board ):
        #question how to remember the state in the tree
        print "Start MTCSPlayer iter = 100"
        #print random.__file__
        m = UCT(rootboard = board, itermax = 2000, player = self, verbose = False)
        #Expend ply level
        #for m in board.legalMoves( self ):
        #nb = deepcopy(board)
        #nb.makeMove(self, m)
            #sm[i+1] = SimulateThread(nb,event)
            #sm[i+1].start()
        #Simulate game by all moves on this level and untile timer end
        
        
        #Backpropagate
        
        
        #Select the best child to doMove

        return m

class Node:
    """ A node in the game tree. Note wins is always from the viewpoint of playerJustMoved.
        Crashes if state not specified.
        """
    def __init__(self, player, move = None, parent = None, board = None):
        self.move = move # the move that got us to this node - "None" for the root node
        self.parentNode = parent # "None" for the root node
        self.childNodes = []
        self.wins = 0
        self.visits = 0
        self.board = board
        self.untriedMoves = board.legalMoves(player) # future child nodes
        self.player = player
    
    def UCTSelectChild(self):
        """ Use the UCB1 formula to select a child node. Often a constant UCTK is applied so we have
            lambda c: c.wins/c.visits + UCTK * sqrt(2*log(self.visits)/c.visits to vary the amount of
            exploration versus exploitation.
            """
        s = sorted(self.childNodes, key = lambda c: c.wins/c.visits + sqrt(2*log(self.visits)/c.visits))[-1]
        return s
    
    def AddChild(self, m, s, p):
        """ Remove m from untriedMoves and add a new child node for this move.
            Return the added child node
            """
        n = Node(move = m, player = p, parent = self, board = s, )
        self.untriedMoves.remove(m)
        self.childNodes.append(n)
        return n
    
    def Update(self, result):
        """ Update this node - one additional visit and result additional wins. result must be from the viewpoint of playerJustmoved.
            """
        self.visits += 1
        self.wins += result
    
    def __repr__(self):
        return "[M:" + str(self.move) + " W/V:" + str(self.wins) + "/" + str(self.visits) + " U:" + str(self.untriedMoves) + "]"
    
    def TreeToString(self, indent):
        s = self.IndentString(indent) + str(self)
        for c in self.childNodes:
            s += c.TreeToString(indent+1)
        return s
    
    def IndentString(self,indent):
        s = "\n"
        for i in range (1,indent+1):
            s += "| "
        return s
    
    def ChildrenToString(self):
        s = ""
        for c in self.childNodes:
            s += str(c) + "\n"
        return s


def UCT(rootboard, itermax, player, verbose = False):
    """ Conduct a UCT search for itermax iterations starting from rootstate.
        Return the best move from the rootstate.
        Assumes 2 alternating players (player 1 starts), with game results in the range [0.0, 1.0]."""
    
    rootnode = Node(board = rootboard, player = player)
    rootplayer = player
    
    print "UCT start"
    
    for i in range(itermax):
        node = rootnode
        board = deepcopy(rootboard)
        #nodeplayer = rootplayer
        
        # Select
        while node.untriedMoves == [] and node.childNodes != []: # node is fully expanded and non-terminal
            node = node.UCTSelectChild()
            board.makeMove(node.player, node.move)
        
        
        # Expand
        if node.untriedMoves != []: # if we can expand (i.e. state/node is non-terminal)
            m = random.choice(node.untriedMoves)
            
            board.makeMove(node.player,m)
            #change to oppenent to move
            nodeplayer = Player(node.player.opp, node.player.type, node.player.ply)
            node = node.AddChild(m,board,nodeplayer) # add child and descend tree
        
        # Rollout - this can often be made orders of magnitude quicker using a state.GetRandomMove() function
        while board.gameOver() != True : # while state is non-terminal
            m = random.choice(board.legalMoves(nodeplayer))
            board.makeMove(nodeplayer, m )
            #print "Simulate Game player:"+str(nodeplayer.num)+"Moves:"+str(m)
            nodeplayer = Player(nodeplayer.opp, nodeplayer.type, nodeplayer.ply)

        # Backpropagate
        while node != None: # backpropagate from the expanded node and work back to the root node
            if board.hasWon(rootplayer.num):
                win = 1
            else :
                win = 0
            node.Update(win) # state is terminal. Update node with result from POV of node.playerJustMoved
            node = node.parentNode
    
    return sorted(rootnode.childNodes, key = lambda c: c.visits)[-1].move # return the move that was most visited







