import Move as m
import Piece as p
import numpy as np
import copy

wk = "\u2654"
wq = "\u2655"
wr = "\u2656"
wb = "\u2657"
wn = "\u2658"
wp = "\u2659"
bk = "\u265A"
bq = "\u265B"
br = "\u265C"
bb = "\u265D"
bn = "\u265E"
bp = "\u265F"
em = "--"

class State(object):
    def __init__(self):
        self.blackPieces=[]
        self.whitePieces=[]
        self.board=np.chararray((8,8),unicode=True,itemsize=2)
        self.board[:]=em
        self.turnNum =1
        # queen =9, 2xrook =10, 2xbishop =6, 2xknight =6, 8xpawn =8
        self.wmat =39
        self.bmat =39
        
    def generateSuccessor(self,move):
        new = copy.deepcopy(self)
        if move.cap=="x":
            pieces=[]
            if new.turnNum%2==1:
                pieces=new.whitePieces
            else:
                pieces=new.blackPieces
            for piece in pieces:
                if piece.x==move.ex and piece.y==move.ey:
                    pieces.remove(piece)
                    if new.turnNum%2==1:
                        new.bmat-=piece.value
                    else:
                        new.wmat-=piece.value
                    
        
        new.board[move.sy][move.sx] = em
        new.board[move.ey][move.ex] = move.piece
        return new
    
    
    def generateMoves(self):
        valid_moves = []
        pieces =[]
        if self.turnNum%2==1:
            pieces = self.whitePieces
        else:
            pieces = self.blackPieces
            
        for piece in pieces:
            if piece.type == bq or piece.type== wq:
                thing=1
        
        
   
    def __str__(self):
        return str(self.board)+"\n"
    def setup_vanilla(self):
        self.board[0,(0,7)] = br
        self.board[0,(1,6)] = bn
        self.board[0,(2,5)] = bb
        self.board[0,3] = bq
        self.board[0,4] = bk
        self.board[1,:] = bp
        self.blackPieces.append(p.Piece(br,0,0,5))
        self.blackPieces.append(p.Piece(br,7,0,5))
        
        self.board[7,(0,7)] = wr
        self.board[7,(1,6)] = wn
        self.board[7,(2,5)] = wb
        self.board[7,3] = wq
        self.board[7,4] = wk
        self.board[6,:] = wp
        
        
  