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
import timeit
import random


INFINITY = 1.0e400


#class SimulateThread(threading.Thread):
#    def __init__(self,board,event):
#        super(SimulateThread, self).__init__()
#        self.board=board
#        self.event=event

#    def run(self):
        #run the simulate process while (1) untile event comes then end
        #update the tree by call update in the tree(need the lock)

class MTCSPlayer(Player):
    def __init__(self, playerNum, playerType, time =10, ply=2):
        self.num = playerNum
        self.opp = 2 - playerNum + 1
        self.type = playerType
        self.time = time;#seconds for simulation
        self.ply = ply
    
    def __repr__(self):
        return str(self.num)
    


    def chooseMove( self, board ):
        #question how to remember the state in the tree
        print "Start MTCSPlayer iter = 10000"
        start = timeit.default_timer()


        #print random.__file__
        m = UCT(rootboard = board, itermax = 2000, player = self, ply = self.ply, verbose = True)
        
        stop = timeit.default_timer()
        
        print "End MCTS Player choose Move:"+str(m)
        print "Use Time:"+str(stop - start) +"Seconds"


        return m
def winlose(rootplayer, board):
    s1 =0.0
    s2 =0.0
    
    
    if board.scoreCups[rootplayer.num-1] > 24:
        return INFINITY
    
    if board.scoreCups[rootplayer.opp-1] > 24:
        return -INFINITY

    s1 = board.scoreCups[rootplayer.num-1]

    #opp Mancala
    s2 = board.scoreCups[rootplayer.opp-1]
    return (s1 - s2) / 48.0

def score(rootplayer, board):
    """ Evaluate the Mancala board for this player """
    # Currently this function just calls Player's score
    # function.  You should replace the line below with your own code
    # for evaluating the board
    #print "MancalaGuru score"
    if rootplayer.num == 1:
        Cups = board.P1Cups
        oppCups = board.P2Cups
    else:
        Cups = board.P2Cups
        oppCups = board.P1Cups
    s1 =0.0
    s2 =0.0
    for i in range(len(Cups)):
        s1 = s1 + Cups[i]*1.0

    s1 = s1+board.scoreCups[rootplayer.num-1]*5.5
    if board.scoreCups[rootplayer.num-1] >24:
        return 1
    #opp cups
    for i in range(len(oppCups)):
        s2 = s2 + oppCups[i]*1.0

                            
    #opp Mancala
    s2 = s2+board.scoreCups[rootplayer.opp-1]*5.5
    if board.scoreCups[rootplayer.opp-1] >24:
        return -1
    
    value = s1 - s2
    return (value)/(48*5.5)
def CatchMove(playerNum, board, move):
    if playerNum == 1:
        Cups = board.P1Cups
        oppCups = board.P2Cups
    else:
        Cups = board.P2Cups
        oppCups = board.P1Cups

    if Cups[move-1]>1 and oppCups[5-move+1]==0:
        for i in range(len(oppCups)):
            if oppCups[i] == 0:
                continue
            if oppCups[i]+i <=5:
                if oppCups[i]+i == 5-move+1:
                    print "Traps for:"+str(playerNum)+" cup="+str(move)+" oppcup="+str(i+1)
                    return True, i
            elif oppCups[i]+i >=13:
                if oppCups[i]+i -13 == 5-move+1:
                    print "Traps for:"+str(playerNum)+" cup="+str(move)+" oppcup="+str(i+1)
                    return True, i
    return False, -1
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
        self.minimax = True
        self.evalue = 0.0
        self.alpha = 0.15
        self.again = False
        self.rvalue = 0.0
    
    def UCTSelectChild(self):
        """ Use the UCB1 formula to select a child node. Often a constant UCTK is applied so we have
            lambda c: c.wins/c.visits + UCTK * sqrt(2*log(self.visits)/c.visits to vary the amount of
            exploration versus exploitation.
            """
        '''MCST UCB1 formula
        '''
        #s = sorted(self.childNodes, key = lambda c: c.wins/c.visits + sqrt(2*log(self.visits)/c.visits))[-1]
        '''MCST Heuristic Implict
        '''
        s = sorted(self.childNodes, key = lambda c: (1-c.alpha)*(c.wins/c.visits)+ c.alpha*c.evalue + sqrt(2*log(self.visits)/c.visits))[-1]
        '''MCST Slover
        '''
        #s = sorted(self.childNodes, key = lambda c: c.rvalue + sqrt(2*log(self.visits)/c.visits+ 0.0005/c.visits))[-1]
        return s
    
    def AddChild(self, m, s, p, v, r, a):
        """ Remove m from untriedMoves and add a new child node for this move.
            Return the added child node
            """
        n = Node(move = m, player = p, parent = self, board = s)
        n.evalue = v
        n.again = a
        if a:
            n.minimax =  self.minimax
        else:
            n.minimax = not self.minimax
        n.rvalue = r
        self.untriedMoves.remove(m)
        self.childNodes.append(n)
        return n
    
    def Update(self, win, lose):
        """ Update this node - one additional visit and result additional wins. result must be from the viewpoint of playerJustmoved.
            """
        vis= win + lose
        self.visits += (win + lose)
        self.wins += win
        #print "Update Win="+str(self.wins)+" Visit="+str(self.visits)
    
    def __repr__(self):
        return "[M:" + str(self.move) + " W/V:" + str(self.wins) + "/" + str(self.visits)  +" P:"+ str(self.player.num)+" H:"+str(self.evalue)+" R:"+str(self.rvalue)+"]\n"
    
    def TreeToString(self, indent, ply):
        if ply == 0:
            return " "
        s = self.IndentString(indent) + str(self)
        for c in self.childNodes:
            s += c.TreeToString(indent+1, ply-1)
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


def UCT(rootboard, itermax, player, ply ,verbose = False):
    """ Conduct a UCT search for itermax iterations starting from rootstate.
        Return the best move from the rootstate.
        Assumes 2 alternating players (player 1 starts), with game results in the range [0.0, 1.0]."""
    
    rootnode = Node(board = rootboard, player = player)
    rootplayer = deepcopy(player)
    
    if rootplayer.num == 1:
        Cups = rootboard.P1Cups
        oppCups = rootboard.P2Cups
    else:
        Cups = rootboard.P2Cups
        oppCups = rootboard.P1Cups
    #print "UCT start point from here"
    print rootboard
    for i in range(itermax):
        if i % 5000 == 0:
            print "Processing :"+str(i)+"/"+str(itermax)
        node = rootnode
        board = deepcopy(rootboard)
        #nodeplayer = rootplayer
        
        
        #if there is already a win move found only when root node fully expliored
        if rootnode.childNodes !=[] and node.childNodes != [] and rootnode.visits == 100:
            for c in rootnode.childNodes:
                #find a win, move that win
                if c.rvalue == 1:
                    return c.move
                #find a bourns move explor for more again moves
                if c.again == True:
                    s, m = rootplayer.alphaBetaMove(rootboard,2)
                    print "Again c.Move="+str(c.move)+" MiniMax ply=2 Move="+str(m)
                    return m
                #find a catch or be catched
                ca, cm = CatchMove(rootplayer.num,rootboard,c.move)
                if ca:
                    return c.move
                ca, cm = CatchMove(rootplayer.opp,rootboard,c.move)
                if ca:
                    return cm
        # Select
        while node.untriedMoves == [] and node.childNodes != []: # node is fully expanded and non-terminal
            node = node.UCTSelectChild()
            board.makeMove(node.player, node.move)
            #print "Select Start Player:"+str(node.player.num)+" Move:"+str(node.move)
        
        
        # Expand
        if node.untriedMoves != []: # if we can expand (i.e. state/node is non-terminal)

            m = random.choice(node.untriedMoves)
            
            again = board.makeMove(node.player,m)
            #print "Expand make move Player:"+str(node.player.num)+" Move:"+str(m)
            #change to oppenent to move
            if again :
                nodeplayer = Player(node.player.num, node.player.type, node.player.ply)
            else :
                nodeplayer = Player(node.player.opp, node.player.type, node.player.ply)
            #print "Expand AddChild Player:"+str(nodeplayer.num)+" Move:"+str(m)
            rvalue = INFINITY
            evalue = score(rootplayer,board)
            rvalue = winlose(rootplayer,board)
            node = node.AddChild(m,board,nodeplayer,evalue,rvalue,again) # add child and descend tree
        
        # Rollout - this can often be made orders of magnitude quicker using a state.GetRandomMove() function
        while board.gameOver() != True : # while state is non-terminal
            if board.scoreCups[rootplayer.num-1]>24 or  board.scoreCups[rootplayer.opp-1]>24:
                break
            #Minimax Hybird Choice with 1 or 2 ply
            s,m = nodeplayer.alphaBetaMove(board,1)
            
            # Random Choice
            #m = random.choice(board.legalMoves(nodeplayer))

            again = board.makeMove(nodeplayer, m )
            #print board
            if again :
                nodeplayer = Player(nodeplayer.num, nodeplayer.type, nodeplayer.ply)
            else :
                nodeplayer = Player(nodeplayer.opp, nodeplayer.type, nodeplayer.ply)


        # Backpropagate
        if board.scoreCups[rootplayer.num-1] >= board.scoreCups[rootplayer.opp-1]:
            win = 1
            lose = 0
        else :
            win = 0
            lose = 1

        while node != None: # backpropagate from the expanded node and work back to the root node
            node.Update(win, lose) # state is terminal. Update node with result from POV of node.playerJustMoved
            if node.childNodes != []:
                #update rvalue to backpropagate
                '''
                rvalue = 0.0
                losetime = 0
                haswin = False
                haslose = False
                hasavarge = False
                for c in node.childNodes:
                    if c.rvalue == -INFINITY:
                        haslose = True
                        losetime +=1
                    if c.rvalue == INFINITY:
                       haswin == True
                       losetime -=1
                    if c.rvalue != INFINITY and  c.rvalue != -INFINITY:
                        hasavarge = True
                        rvalue +=c.rvalue

                if haswin and not haslose:
                    node.rvalue = INFINITY
                elif haslose and not haswin and not hasavarge :
                    node.rvalue = -INFINITY
                elif haslose and hasavarge:
                    node.rvalue = (rvalue -losetime)/len(node.childNodes)
                else:
                    node.rvalue = rvalue/len(node.childNodes)
                '''
                #update evalue to backpropagate
                if node.minimax == True:
                    node.evalue = sorted(node.childNodes, key =lambda c: c.evalue)[-1].evalue
                    #node.rvalue = sorted(node.childNodes, key =lambda c: c.rvalue)[-1].rvalue
                else :
                    node.evalue = sorted(node.childNodes, key=lambda c: c.evalue)[0].evalue
                    #node.rvalue = sorted(node.childNodes, key =lambda c: c.rvalue)[0].rvalue

            node = node.parentNode
    print rootnode.TreeToString(0,3)
    '''MCST Heuristic Implict
    '''
    #return sorted(rootnode.childNodes, key = lambda c: c.visits)[-1].move
    '''MCST Slover
    '''
    #return sorted(rootnode.childNodes, key = lambda c: c.rvalue+1/sqrt(c.visits))[-1].move
    '''MCST UCB1 most visited
    '''
    return sorted(rootnode.childNodes, key = lambda c: c.visits)[-1].move # return the move that was most visited
































