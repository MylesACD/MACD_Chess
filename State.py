import Move as m
import Piece as p
import numpy as np
import copy
import time
import sys

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

white =1
black =0

#testing variables
#-----------------
check_time = 0
deep_copy_time = 0
move_time = 0 



#-----------------

def get_color(piece_type):
   rep = hex(ord(piece_type))
   if int(rep,16) < 0x265A:
       return 1
   else:
       return 0

class State():
    def __init__(self):
        self.blackPieces=[]
        self.whitePieces=[]
        self.board=np.chararray((8,8),unicode=True,itemsize=4)
        self.board[:]=em
        self.turnNum =1
        # queen =9, 2xrook =10, 2xbishop =6, 2xknight =6, 8xpawn =8
        self.wmat =0
        self.bmat =0
        self.previousMove=None
        self.draw_timer = 0
        # first value for wether or not there is an outcome
        # 0 for draw, 100 for white win, -100 for black
        self.outcome = [False,0]
        
    def deep_clone(self):
        clone  = State()
        clone.board = copy.deepcopy(self.board)
        for piece in self.whitePieces:
            clone.whitePieces.append(piece.deep_clone())
        for piece in self.blackPieces:
            clone.blackPieces.append(piece.deep_clone())     
      
        if self.previousMove is not None:
            clone.previousMove = self.previousMove.deep_clone()
        clone.wmat = self.wmat
        clone.bmat = self.bmat
        clone.turnNum = self.turnNum
        return clone
        
        
    def generateSuccessor(self,move):
        global deep_copy_time
        t = time.perf_counter()
        new = self.deep_clone()
        deep_copy_time += (time.perf_counter()-t)
        curr_pieces=[]
        other_pieces=[]
        if new.turnNum%2==white:
            curr_pieces=new.whitePieces
            other_pieces = new.blackPieces
        else:
            other_pieces=new.whitePieces
            curr_pieces = new.blackPieces
        # remove a captured piece
        if move.cap=="x":
            new.draw_timer = 0
            for piece in other_pieces:
                if piece.x==move.ex and piece.y==move.ey:
                    other_pieces.remove(piece)
                    if new.turnNum%2==white:
                        new.bmat-=piece.value
                    else:
                        new.wmat-=piece.value
                    break
        # if not capture and not a pawn move
        elif move.piece.type!=bp and move.piece.type != wp:
            new.draw_timer +=1    
        else:
            new.draw_timer = 0 
        # update the piece(s) that moved
        new.board[move.sy][move.sx] = em
        new.board[move.ey][move.ex] = move.piece.type
        
    
        # castling case
        if "O" in move.extra:
            
            y=0
            if new.turnNum%2==white:
                y=7

            else:
                y=0
                
            # long castle
            if "O-O-O" in move.extra:
                rook  = [piece for piece in curr_pieces if piece.x==0 and (piece.y==0 or piece.y==7)][0]
                
                new.board[y,3] = rook.type
                new.board[y,0] = em
                rook.x = 3
                
            # short castle
            else:
               
                rook  = [piece for piece in curr_pieces if piece.x==7 and (piece.y==0 or piece.y==7)][0]
                #print(rook)
                new.board[y,5] = rook.type
                new.board[y,7] = em
                rook.x = 5
              
        #promotion case
        elif "=" in move.extra:
            # depending on color
            # change the display on the board
            # find the piece in the piece lists and update its type
            piece = [piece for piece in curr_pieces if piece.x==move.sx and piece.y==move.sy][0]
     
            if new.turnNum%2==1:
                if "Q" in move.extra:
                    piece.type = wq
                    piece.value = 9
                    new.wmat+=8
                elif "B" in move.extra:
                    piece.type=wb
                    piece.value = 3
                    new.wmat+=2
                elif "N" in move.extra:
                    piece.type=wn
                    piece.value = 3
                    new.wmat+=2
                elif "R" in move.extra:
                    piece.type=wr
                    piece.value = 5
                    new.wmat+=4
                    
            else:
                if "Q" in move.extra:
                    piece.type = bq
                    piece.value = 9
                    new.bmat+=8
                elif "B" in move.extra:
                    piece.type=bb
                    piece.value = 3
                    new.bmat+=2
                elif "N" in move.extra:
                    piece.type=bn
                    piece.value = 3
                    new.bmat+=2
                elif "R" in move.extra:
                    piece.type=br
                    piece.value = 5
                    new.bmat+=4
                
            new.board[move.ey,move.ex] ==piece.type
        # update the piece referred to by move
        for piece in curr_pieces:
                
            if piece.x==move.sx and piece.y==move.sy:
                piece.x = move.ex
                piece.y=move.ey
                piece.has_not_moved = False
                break
          
        
        
        new.previousMove = move
        new.turnNum+=1
        return new
    
    # generate all possible moves for a player's turn including self checks
    # to be actually playable these moves will have to filtered
    def generate_all_moves(self, check=True):
        start = time.perf_counter()
        all_moves = []
        pieces =[]
        if self.turnNum%2==1:
            pieces = self.whitePieces
        else:
            pieces = self.blackPieces
        
        for piece in pieces:
            
            #White Pawn Case
            if piece.type == wp:
                # move 1 forward
                if piece.y-1>=0 and self.board[piece.y-1,piece.x]==em:
                    all_moves.append(m.Move(piece,piece.x,piece.y,"",piece.x,piece.y-1,""))
                # move 2 forward   
                if piece.y == 6 and self.board[piece.y-1,piece.x]==em and self.board[piece.y-2,piece.x]==em:
                   all_moves.append(m.Move(piece,piece.x,piece.y,"",piece.x,piece.y-2,""))
                
                # take left
                if piece.x>0 and self.board[piece.y-1,piece.x-1]!=em and get_color(self.board[piece.y-1,piece.x-1]) != piece.color:
                   all_moves.append(m.Move(piece, piece.x, piece.y, "x", piece.x-1, piece.y-1,""))
                
                # take right
                if piece.x<7 and self.board[piece.y-1,piece.x+1]!=em and get_color(self.board[piece.y-1,piece.x+1]) != piece.color:
                    all_moves.append(m.Move(piece, piece.x, piece.y, "x", piece.x+1, piece.y-1,""))
                #en passant
                if self.previousMove and piece.y == 3 and self.previousMove.piece.type == bp and self.previousMove.ey - self.previousMove.sy == 2 and (self.previousMove.ex == piece.x - 1 or self.previousMove.ex == piece.x + 1): 
                    all_moves.append(m.Move(piece, piece.x, piece.y, "x",self.previousMove.ex, self.previousMove.ey - 1,""))

            #Black Pawn Case
            elif piece.type == bp:
                 # move 1 forward
                if piece.y+1<=7 and self.board[piece.y+1,piece.x]==em:
                    all_moves.append(m.Move(piece,piece.x,piece.y,"",piece.x,piece.y+1,""))
                # move 2 forward   
                if piece.y == 1 and self.board[piece.y+1,piece.x]==em and self.board[piece.y+2,piece.x]==em:
                   all_moves.append(m.Move(piece,piece.x,piece.y,"",piece.x,piece.y+2,""))
                
                # take left
                if piece.x>0 and self.board[piece.y+1,piece.x-1]!=em and get_color(self.board[piece.y+1,piece.x-1]) != piece.color:
                   all_moves.append(m.Move(piece, piece.x, piece.y, "x", piece.x-1, piece.y+1,""))
                
                # take right
                if piece.x<7 and self.board[piece.y+1,piece.x+1]!=em and get_color(self.board[piece.y+1,piece.x+1]) != piece.color:
                    all_moves.append(m.Move(piece, piece.x, piece.y, "x", piece.x+1, piece.y+1,""))
                #en passant
                if self.previousMove and piece.y == 4 and self.previousMove.piece.type == wp and self.previousMove.ey - self.previousMove.sy == -2 and (self.previousMove.ex == piece.x - 1 or self.previousMove.ex == piece.x + 1): 
                    all_moves.append(m.Move(piece, piece.x, piece.y, "x",self.previousMove.ex, self.previousMove.ey + 1,""))

                
            
            # All Bishop Case
            elif piece.type == wb or piece.type ==bb:
                # move nw
                tempx = piece.x - 1
                tempy = piece.y - 1
                # while the x,y are within the board
                while tempx > -1 and tempx < 8 and tempy > -1 and tempy < 8:
                    # if the space is empty
                    if self.board[tempy,tempx]==em:
                        all_moves.append(m.Move(piece,piece.x,piece.y,"",tempx,tempy,""))
                        tempx-=1
                        tempy-=1
                    
                    else: 
                        # if there is a piece and their color does not match
                        if get_color(self.board[tempy,tempx]) != piece.color:
                            all_moves.append(m.Move(piece,piece.x,piece.y,"x",tempx,tempy,""))
                        # there is a piece blocking wether opponent or not
                        break
                # move sw
                tempx = piece.x - 1
                tempy = piece.y + 1
                # while the x,y are within the board
                while tempx > -1 and tempx < 8 and tempy > -1 and tempy < 8:
                    # if the space is empty
                    if self.board[tempy,tempx]==em:
                        all_moves.append(m.Move(piece,piece.x,piece.y,"",tempx,tempy,""))
                        tempx-=1
                        tempy+=1
                    
                    else: 
                        # if there is a piece and their color does not match
                        if get_color(self.board[tempy,tempx]) != piece.color:
                            all_moves.append(m.Move(piece,piece.x,piece.y,"x",tempx,tempy,""))
                        # there is a piece blocking wether opponent or not
                        break
                # move ne
                tempx = piece.x + 1
                tempy = piece.y - 1
                # while the x,y are within the board
                while tempx > -1 and tempx < 8 and tempy > -1 and tempy < 8:
                    # if the space is empty
                    if self.board[tempy,tempx]==em:
                        all_moves.append(m.Move(piece,piece.x,piece.y,"",tempx,tempy,""))
                        tempx+=1
                        tempy-=1
                    
                    else: 
                        # if there is a piece and their color does not match
                        if get_color(self.board[tempy,tempx]) != piece.color:
                            all_moves.append(m.Move(piece,piece.x,piece.y,"x",tempx,tempy,""))
                        # there is a piece blocking wether opponent or not
                        break
                    # move se
                tempx = piece.x + 1
                tempy = piece.y + 1
                # while the x,y are within the board
                while tempx > -1 and tempx < 8 and tempy > -1 and tempy < 8:
                    # if the space is empty
                    if self.board[tempy,tempx]==em:
                        all_moves.append(m.Move(piece,piece.x,piece.y,"",tempx,tempy,""))
                        tempx+=1
                        tempy+=1
                    
                    else: 
                        # if there is a piece and their color does not match
                        if get_color(self.board[tempy,tempx]) != piece.color:
                            all_moves.append(m.Move(piece,piece.x,piece.y,"x",tempx,tempy,""))
                        # there is a piece blocking wether opponent or not
                        break
                    
            # Knights        
            elif piece.type == wn or piece.type == bn:
                # north jump, left
                tempx = piece.x - 1
                tempy = piece.y - 2
                if tempx > -1 and tempx < 8 and tempy > -1 and tempy < 8:
                    if self.board[tempy][tempx] == em :
                        all_moves.append(m.Move(piece,piece.x,piece.y,"",tempx,tempy,""))
                    elif get_color(self.board[tempy,tempx])!= piece.color :
                        all_moves.append(m.Move(piece,piece.x,piece.y,"x",tempx,tempy,""))
                # north jump, right
                tempx = piece.x + 1
                tempy = piece.y - 2
                if tempx > -1 and tempx < 8 and tempy > -1 and tempy < 8:
                    if self.board[tempy][tempx] == em :
                        all_moves.append(m.Move(piece,piece.x,piece.y,"",tempx,tempy,""))
                    elif get_color(self.board[tempy,tempx])!= piece.color :
                        all_moves.append(m.Move(piece,piece.x,piece.y,"x",tempx,tempy,""))
                # south jump, left
                tempx = piece.x - 1
                tempy = piece.y + 2
                if tempx > -1 and tempx < 8 and tempy > -1 and tempy < 8:
                    if self.board[tempy][tempx] == em :
                        all_moves.append(m.Move(piece,piece.x,piece.y,"",tempx,tempy,""))
                    elif get_color(self.board[tempy,tempx])!= piece.color :
                        all_moves.append(m.Move(piece,piece.x,piece.y,"x",tempx,tempy,""))
                # south jump, right
                tempx = piece.x + 1
                tempy = piece.y + 2
                if tempx > -1 and tempx < 8 and tempy > -1 and tempy < 8:
                    if self.board[tempy][tempx] == em :
                        all_moves.append(m.Move(piece,piece.x,piece.y,"",tempx,tempy,""))
                    elif get_color(self.board[tempy,tempx])!= piece.color :
                        all_moves.append(m.Move(piece,piece.x,piece.y,"x",tempx,tempy,""))
                        
                # right jump, up
                tempx = piece.x + 2
                tempy = piece.y - 1
                if tempx > -1 and tempx < 8 and tempy > -1 and tempy < 8:
                    if self.board[tempy][tempx] == em :
                        all_moves.append(m.Move(piece,piece.x,piece.y,"",tempx,tempy,""))
                    elif get_color(self.board[tempy,tempx])!= piece.color :
                        all_moves.append(m.Move(piece,piece.x,piece.y,"x",tempx,tempy,""))
                # right jump, down
                tempx = piece.x + 2
                tempy = piece.y + 1
                if tempx > -1 and tempx < 8 and tempy > -1 and tempy < 8:
                    if self.board[tempy][tempx] == em :
                        all_moves.append(m.Move(piece,piece.x,piece.y,"",tempx,tempy,""))
                    elif get_color(self.board[tempy,tempx])!= piece.color :
                        all_moves.append(m.Move(piece,piece.x,piece.y,"x",tempx,tempy,""))
                # left jump, up
                tempx = piece.x - 2
                tempy = piece.y - 1
                if tempx > -1 and tempx < 8 and tempy > -1 and tempy < 8:
                    if self.board[tempy][tempx] == em :
                        all_moves.append(m.Move(piece,piece.x,piece.y,"",tempx,tempy,""))
                    elif get_color(self.board[tempy,tempx])!= piece.color :
                        all_moves.append(m.Move(piece,piece.x,piece.y,"x",tempx,tempy,""))
                # left jump, down
                tempx = piece.x - 2
                tempy = piece.y + 1
                if tempx > -1 and tempx < 8 and tempy > -1 and tempy < 8:
                    if self.board[tempy][tempx] == em :
                        all_moves.append(m.Move(piece,piece.x,piece.y,"",tempx,tempy,""))
                    elif get_color(self.board[tempy,tempx])!= piece.color :
                        all_moves.append(m.Move(piece,piece.x,piece.y,"x",tempx,tempy,""))
                    
            
  
            elif piece.type ==wr or piece.type==br:
                # move up
                tempy = piece.y - 1
                while tempy > -1 and tempy < 8:
                    # move into empty space
                    if self.board[tempy][piece.x] == em :
                        all_moves.append(m.Move(piece,piece.x,piece.y,"",piece.x,tempy,""))
                        
                    # take enemy peice    
                    else:
                    
                        if get_color(self.board[tempy][piece.x])!=piece.color: 
                            all_moves.append(m.Move(piece,piece.x,piece.y,"x",piece.x,tempy,""))
                        break
                    tempy-=1
                
                 # move down
                tempy = piece.y + 1
                while tempy > -1 and tempy < 8:
                    # move into empty space
                    if self.board[tempy][piece.x] == em :
                        all_moves.append(m.Move(piece,piece.x,piece.y,"",piece.x,tempy,""))
                        
                    # take enemy peice    
                    else:
                        if get_color(self.board[tempy][piece.x])!=piece.color: 
                            all_moves.append(m.Move(piece,piece.x,piece.y,"x",piece.x,tempy,""))
                    
                        break
                    tempy+=1
                    

               # move right
                tempx = piece.x + 1
                while tempx > -1 and tempx < 8:
                    # move into empty space
                    if self.board[piece.y][tempx] == em :
                        all_moves.append(m.Move(piece,piece.x,piece.y,"",tempx,piece.y,""))
                        
                    # take enemy peice    
                    else:
                        if get_color(self.board[piece.y][tempx])!=piece.color: 
                            all_moves.append(m.Move(piece,piece.x,piece.y,"x",tempx,piece.y,""))
                        break
                    tempx+=1
                    
                # move left
                tempx = piece.x -1 
                while tempx > -1 and tempx < 8:
                    # move into empty space
                    if self.board[piece.y][tempx] == em :
                        all_moves.append(m.Move(piece,piece.x,piece.y,"",tempx,piece.y,""))
                        
                     #there is a piece there  
                    else: 
                        # take enemy peice 
                        if get_color(self.board[piece.y][tempx])!=piece.color: 
                            all_moves.append(m.Move(piece,piece.x,piece.y,"x",tempx,piece.y,""))
                        break
                    tempx-=1
    
                    

             
            elif piece.type==bq or piece.type==wq:
                # move up
                tempy = piece.y - 1
                while tempy > -1 and tempy < 8:
                    # move into empty space
                    if self.board[tempy][piece.x] == em :
                        all_moves.append(m.Move(piece,piece.x,piece.y,"",piece.x,tempy,""))
                        
                    # take enemy peice    
                    else:
                    
                        if get_color(self.board[tempy][piece.x])!=piece.color: 
                            all_moves.append(m.Move(piece,piece.x,piece.y,"x",piece.x,tempy,""))
                        break
                    tempy-=1
                
                 # move down
                tempy = piece.y + 1
                while tempy > -1 and tempy < 8:
                    # move into empty space
                    if self.board[tempy][piece.x] == em :
                        all_moves.append(m.Move(piece,piece.x,piece.y,"",piece.x,tempy,""))
                        
                    # take enemy peice    
                    else:
                        if get_color(self.board[tempy][piece.x])!=piece.color: 
                            all_moves.append(m.Move(piece,piece.x,piece.y,"x",piece.x,tempy,""))
                    
                        break
                    tempy+=1
                    

               # move right
                tempx = piece.x + 1
                while tempx > -1 and tempx < 8:
                    # move into empty space
                    if self.board[piece.y][tempx] == em :
                        all_moves.append(m.Move(piece,piece.x,piece.y,"",tempx,piece.y,""))
                        
                       
                    else:
                         # take enemy peice
                        if get_color(self.board[piece.y][tempx])!=piece.color: 
                            all_moves.append(m.Move(piece,piece.x,piece.y,"x",tempx,piece.y,""))
                        break
                    tempx+=1
                    
                # move left
                tempx = piece.x -1 
                while tempx > -1 and tempx < 8:
                    # move into empty space
                    if self.board[piece.y][tempx] == em :
                        all_moves.append(m.Move(piece,piece.x,piece.y,"",tempx,piece.y,""))
                        
                     #there is a piece there  
                    else: 
                        # take enemy peice 
                        if get_color(self.board[piece.y][tempx])!=piece.color: 
                            all_moves.append(m.Move(piece,piece.x,piece.y,"x",tempx,piece.y,""))
                        break
                    tempx-=1
                    
                # move nw
                tempx = piece.x - 1
                tempy = piece.y - 1
                # while the x,y are within the board
                while tempx > -1 and tempx < 8 and tempy > -1 and tempy < 8:
                    # if the space is empty
                    if self.board[tempy,tempx]==em:
                        all_moves.append(m.Move(piece,piece.x,piece.y,"",tempx,tempy,""))
                        tempx-=1
                        tempy-=1
                    
                    else: 
                        # if there is a piece and their color does not match
                        if get_color(self.board[tempy,tempx]) != piece.color:
                            all_moves.append(m.Move(piece,piece.x,piece.y,"x",tempx,tempy,""))
                        # there is a piece blocking wether opponent or not
                        break
                # move sw
                tempx = piece.x - 1
                tempy = piece.y + 1
                # while the x,y are within the board
                while tempx > -1 and tempx < 8 and tempy > -1 and tempy < 8:
                    # if the space is empty
                    if self.board[tempy,tempx]==em:
                        all_moves.append(m.Move(piece,piece.x,piece.y,"",tempx,tempy,""))
                        tempx-=1
                        tempy+=1
                    
                    else: 
                        # if there is a piece and their color does not match
                        if get_color(self.board[tempy,tempx]) != piece.color:
                            all_moves.append(m.Move(piece,piece.x,piece.y,"x",tempx,tempy,""))
                        # there is a piece blocking wether opponent or not
                        break
                # move ne
                tempx = piece.x + 1
                tempy = piece.y - 1
                # while the x,y are within the board
                while tempx > -1 and tempx < 8 and tempy > -1 and tempy < 8:
                    # if the space is empty
                    if self.board[tempy,tempx]==em:
                        all_moves.append(m.Move(piece,piece.x,piece.y,"",tempx,tempy,""))
                        tempx+=1
                        tempy-=1
                    
                    else: 
                        # if there is a piece and their color does not match
                        if get_color(self.board[tempy,tempx]) != piece.color:
                            all_moves.append(m.Move(piece,piece.x,piece.y,"x",tempx,tempy,""))
                        # there is a piece blocking wether opponent or not
                        break
                    # move se
                tempx = piece.x + 1
                tempy = piece.y + 1
                # while the x,y are within the board
                while tempx > -1 and tempx < 8 and tempy > -1 and tempy < 8:
                    # if the space is empty
                    if self.board[tempy,tempx]==em:
                        all_moves.append(m.Move(piece,piece.x,piece.y,"",tempx,tempy,""))
                        tempx+=1
                        tempy+=1
                    
                    else: 
                        # if there is a piece and their color does not match
                        if get_color(self.board[tempy,tempx]) != piece.color:
                            all_moves.append(m.Move(piece,piece.x,piece.y,"x",tempx,tempy,""))
                        # there is a piece blocking wether opponent or not
                        break
                    
                    
            # king moves
            elif piece.type==bk or piece.type==wk:
                # move N
                tempy = piece.y - 1
                if tempy > -1 and tempy < 8:
                    # move into empty space
                    if self.board[tempy][piece.x] == em :
                        all_moves.append(m.Move(piece,piece.x,piece.y,"",piece.x,tempy,""))
                        
                    # take enemy peice    
                    elif get_color(self.board[tempy][piece.x])!=piece.color: 
                        all_moves.append(m.Move(piece,piece.x,piece.y,"x",piece.x,tempy,""))
                        
                # move W
                tempx = piece.x - 1
                if tempx > -1 and tempx < 8:
                    # move into empty space
                    if self.board[piece.y][tempx] == em :
                        all_moves.append(m.Move(piece,piece.x,piece.y,"",tempx,piece.y,""))
                        
                    # take enemy peice    
                    elif get_color(self.board[piece.y][tempx])!=piece.color: 
                        all_moves.append(m.Move(piece,piece.x,piece.y,"x",tempx,piece.y,""))
                        
                # move E
                tempx = piece.x + 1
                if tempx > -1 and tempx < 8:
                    # move into empty space
                    if self.board[piece.y][tempx] == em :
                        all_moves.append(m.Move(piece,piece.x,piece.y,"",tempx,piece.y,""))
                        
                    # take enemy peice    
                    elif get_color(self.board[piece.y][tempx])!=piece.color: 
                        all_moves.append(m.Move(piece,piece.x,piece.y,"x",tempx,piece.y,""))
                
                # move S
                tempy = piece.y + 1
                if tempy > -1 and tempy < 8:
                    # move into empty space
                    if self.board[tempy][piece.x] == em :
                        all_moves.append(m.Move(piece,piece.x,piece.y,"",piece.x,tempy,""))
                        
                    # take enemy peice    
                    elif get_color(self.board[tempy][piece.x])!=piece.color: 
                        all_moves.append(m.Move(piece,piece.x,piece.y,"x",piece.x,tempy,""))
                        
                # move NW
                tempy = piece.y - 1
                tempx = piece.x - 1
                if tempy > -1 and tempy < 8 and tempx > -1 and tempx < 8:
                    # move into empty space
                    if self.board[tempy][tempx] == em :
                        all_moves.append(m.Move(piece,piece.x,piece.y,"",tempx,tempy,""))
                        
                    # take enemy peice    
                    elif get_color(self.board[tempy][tempx])!=piece.color: 
                        all_moves.append(m.Move(piece,piece.x,piece.y,"x",tempx,tempy,""))
                # move SW
                tempy = piece.y + 1
                tempx = piece.x - 1
                if tempy > -1 and tempy < 8 and tempx > -1 and tempx < 8:
                    # move into empty space
                    if self.board[tempy][tempx] == em :
                        all_moves.append(m.Move(piece,piece.x,piece.y,"",tempx,tempy,""))
                        
                    # take enemy peice    
                    elif get_color(self.board[tempy][tempx])!=piece.color: 
                        all_moves.append(m.Move(piece,piece.x,piece.y,"x",tempx,tempy,""))
                        
                # move SE
                tempy = piece.y + 1
                tempx = piece.x + 1
                if tempy > -1 and tempy < 8 and tempx > -1 and tempx < 8:
                    # move into empty space
                    if self.board[tempy][tempx] == em :
                        all_moves.append(m.Move(piece,piece.x,piece.y,"",tempx,tempy,""))
                        
                    # take enemy peice    
                    elif get_color(self.board[tempy][tempx])!=piece.color: 
                        all_moves.append(m.Move(piece,piece.x,piece.y,"x",tempx,tempy,""))
                
                # move NE
                tempy = piece.y - 1
                tempx = piece.x + 1
                if tempy > -1 and tempy < 8 and tempx > -1 and tempx < 8:
                    # move into empty space
                    if self.board[tempy][tempx] == em :
                        all_moves.append(m.Move(piece,piece.x,piece.y,"",tempx,tempy,""))
                        
                    # take enemy peice    
                    elif get_color(self.board[tempy][tempx])!=piece.color: 
                        all_moves.append(m.Move(piece,piece.x,piece.y,"x",tempx,tempy,""))
                
                # castling logic
                x = piece.x
                y = piece.y
                # TODO checking 
                if piece.has_not_moved and self.previousMove is not None and"+" not in self.previousMove.extra:
                    #long castle, checks empty spaces, and that the piece in the corner has not moved
                    if self.board[y,x-1]==em and self.board[y,x-2]==em and self.board[y,x-3]==em and self.get_piece_at_position(x-4, y).has_not_moved:
                        all_moves.append(m.Move(piece,x,y,"",x-2,y,"O-O-O"))
                            
                    #short castle, checks empty spaces, and that the piece in the corner has not moved
                    if self.board[y,x+1]==em and self.board[y,x+2]==em and self.get_piece_at_position(x+3,y).has_not_moved:
                        all_moves.append(m.Move(piece,x,y,"",x+2,y,"O-O"))
                   
        

        #add promotions tags
        for move in all_moves:
            # if the piece is a pawn and at one of the far sides
            if (move.piece.type==wp or move.piece.type==bp) and (move.ey==0 or move.ey==7) and "=" not in move.extra:
                knight = copy.copy(move)
                bishop = copy.copy(move)
                rook = copy.copy(move)
                knight.extra="=N"
                move.extra="=Q"
                bishop.extra="=B"
                rook.extra="=R"
                all_moves.append(knight)
                all_moves.append(bishop)
                all_moves.append(rook)
                
        global move_time
        move_time+=time.perf_counter()-start
        if check==True:
                global check_time
                t = time.perf_counter()
                all_moves = self.filter_self_checks(all_moves)
                check_time += (time.perf_counter()-t)
                
            
        return all_moves
    
    #TODO
    def filter_self_checks(self,all_moves):
        refined =[]
        for move in all_moves:
            valid = True
            # make the next state
            fs = self.generateSuccessor(move)
            # 
            king = fs.get_king_position(self.turnNum%2)
            fmoves = fs.generate_all_moves(False)
            for fm in fmoves:
                if fm.ex ==king[0]  and fm.ey==king[1]:
                    valid=False
                    break
            if valid:
                refined.append(move)
        return refined
    
    # one function call to find all valid moves and then the states from those moves
    # returns a list of new states
    def generate_all_successor_states(self):
        if self.is_terminal():
            return []
        moves= self.generate_all_moves(True)
        states = [self.generateSuccessor(move) for move in moves]
        return states
                
    # returns the piece object at a certain x,y
    def get_piece_at_position(self, x, y):
        for piece in self.blackPieces:
            if piece.x==x and piece.y==y:
                return piece
        for piece in self.whitePieces:
            if piece.x==x and piece.y==y:
                return piece
        rtn = p.Piece(em,-1,-1,-1,-1)
        #to support castling
        rtn.has_not_moved = False
        return rtn
    
    def get_king_position(self, color):
        curr_pieces = []
        if color==white:
            curr_pieces = self.whitePieces
        elif color==black:
            curr_pieces = self.blackPieces
        for piece in curr_pieces:
            if piece.type == bk or piece.type == wk:
                return [piece.x,piece.y]
        # just in case, this should never be reached but hey
        return [-1,-1]

   
    def __str__(self):
        return str(self.board)
    
    def convert_board_to_num(self,mat=False):
        temp = self.board.flatten()
        output=np.zeros(65,dtype=int)
        # white is negative
        # black is positive
        
        #pawn 1
        #knight 3
        #bishop 4
        # rook 5
        # queen 9
        # king 100
        for i in range(len(temp)):
            
            if temp[i]==em:
                output[i+1] = 0
            elif temp[i]== wp:
                output[i+1] = -1
            elif temp[i]== wn:
                output[i+1] = -3
            elif temp[i]== wb:
                output[i+1] = -4
            elif temp[i]== wr:
                output[i+1] = -5
            elif temp[i]== wq:
                output[i+1] = -9
            elif temp[i]== wk:
                output[i+1] = -100
            elif temp[i]== bp:
                output[i+1] = 1
            elif temp[i]== bn:
                output[i+1] = 3
            elif temp[i]== bb:
                output[i+1] = 4
            elif temp[i]== br:
                output[i+1] = 5
            elif temp[i]== bq:
                output[i+1] = 9
            elif temp[i]== bk:
                output[i+1] = 100
                
        output[0] =  self.turnNum%2
        
        if mat:
            output = np.append(output, self.bmat-self.wmat)
        #print(output)
        return output
    
    #TODO
    def is_terminal(self):
        return self.outcome[0] 
    
    # evaluates based on calling player
    def standard_mat_eval(self, color=white):
        if self.outcome[0]:
            return self.outcome[1]
        
        
        if color == white:
            return self.wmat-self.bmat
        else:
            return self.bmat - self.wmat
        
    
    def setup_vanilla(self):
        self.__init__()
        self.wmat =39
        self.bmat =39
        self.board[0,(0,7)] = br
        self.board[0,(1,6)] = bn
        self.board[0,(2,5)] = bb
        self.board[0,3] = bq
        self.board[0,4] = bk
        self.board[1,:] = bp
      
        self.board[7,(0,7)] = wr
        self.board[7,(1,6)] = wn
        self.board[7,(2,5)] = wb
        self.board[7,3] = wq
        self.board[7,4] = wk
        self.board[6,:] = wp
        
        for i in range(8):
            self.blackPieces.append(p.Piece(bp, i, 1, 1, black))
            self.whitePieces.append(p.Piece(wp, i, 6, 1, white))
            
        self.blackPieces.append(p.Piece(br, 0, 0, 5, black))
        self.blackPieces.append(p.Piece(bn, 1, 0, 3, black))
        self.blackPieces.append(p.Piece(bb, 2, 0, 3, black))
        self.blackPieces.append(p.Piece(bq, 3, 0, 9, black))
        self.blackPieces.append(p.Piece(bk, 4, 0, 100, black))
        self.blackPieces.append(p.Piece(bb, 5, 0, 3,black))
        self.blackPieces.append(p.Piece(bn, 6, 0, 3,black))
        self.blackPieces.append(p.Piece(br, 7, 0, 5,black))

        self.whitePieces.append(p.Piece(wr, 0, 7, 5,white))
        self.whitePieces.append(p.Piece(wn, 1, 7, 3,white))
        self.whitePieces.append(p.Piece(wb, 2, 7, 3,white))
        self.whitePieces.append(p.Piece(wq, 3, 7, 9,white))
        self.whitePieces.append(p.Piece(wk, 4, 7, 100,white))
        self.whitePieces.append(p.Piece(wb, 5, 7, 3,white))
        self.whitePieces.append(p.Piece(wn, 6, 7, 3,white))
        self.whitePieces.append(p.Piece(wr, 7, 7, 5,white))
        
def get_op_stats():
    stats_dict = {
        "Check": check_time,
        "Cloning": deep_copy_time,
        "Move Gen": move_time
    }
    return stats_dict