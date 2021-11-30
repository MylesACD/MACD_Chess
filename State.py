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

white =1
black =0

def get_color(piece_type):
   rep = hex(ord(piece_type))
   if int(rep,16) < 0x265A:
       return 1
   else:
       return 0

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
        self.previousMove=None
        
    def generateSuccessor(self,move):
        new = copy.deepcopy(self)
        if move.cap=="x":
            pieces=[]
            if new.turnNum%2==white:
                pieces=new.whitePieces
            else:
                pieces=new.blackPieces
            for piece in pieces:
                if piece.x==move.ex and piece.y==move.ey:
                    pieces.remove(piece)
                    if new.turnNum%2==white:
                        new.bmat-=piece.value
                    else:
                        new.wmat-=piece.value
                    
        
        new.board[move.sy][move.sx] = em
        new.board[move.ey][move.ex] = move.piece
        new.previousMove = move
        new.turnNum+=1
        return new
    """        
    def generateMoves(self):
        valid_moves = []
        pieces =[]
        if self.turnNum%2==1:
            pieces = self.whitePieces
        else:
            pieces = self.blackPieces
        
        for piece in pieces:
            
            #White Pawn Case
            if piece.type == wp:
				# move 1 forward
                
				# move 2 forward
				
				# take left
				
				# take right
				
				# en passant
				
            #Black Pawn Case
            elif piece.type == bp:
				# move 1 forward
				
				# move 2 forward
				
				# take left
				
				# take right
				
				# en passant
                
            # All Bishop Case
            elif piece.type == wb or piece.type ==bb:
				# move nw
				tempx = piece.x - 1
				tempy = piece.y - 1
				# while the x,y are within the board
				while tempx > -1 and tempx < 8 and tempy > -1 and tempy < 8:
					# if the space is empty
					
					# elif there is a piece and their color does not match
					
				# move sw
				tempx = piece.x - 1
				tempy = piece.y + 1
				while tempx > -1 and tempx < 8 and tempy > -1 and tempy < 8:
                    # if the space is empty
					
					# elif there is a piece and their color does not match
				
				# move ne
				tempx = piece.x + 1
				tempy = piece.y - 1
				while tempx > -1 and tempx < 8 and tempy > -1 and tempy < 8: 
    				# if the space is empty
					
					# elif there is a piece and their color does not match
				
				# move se
				tempx = piece.x + 1
				tempy = piece.y + 1
				while tempx > -1 and tempx < 8 and tempy > -1 and tempy < 8: 
					# if the space is empty
					
					# elif there is a piece and their color does not match

			case "r":
			case "R":
				# move up
				tempy = piece.y - 1
				while tempy > -1 and tempy < 8
					# move into empty space
					if self.board[tempy][piece.x] == em :
                        
					# take enemy peice	
					elif self.board[tempy][piece.x]: 
						
					

									
				# move down
    			tempy = piece.y + 1
    				while tempy > -1 and tempy < 8
    					# move into empty space
    					if self.board[tempy][piece.x] == em :
                            
    					# take enemy peice	
    					elif self.board[tempy][piece.x]: 

				
				# move right
    			tempx = piece.x + 1
    				while tempx > -1 and tempx < 8
    					# move into empty space
    					if self.board[piece.y][tempx] == em :
                            
    					# take enemy peice	
    					elif self.board[piece.y][tempx]: 



				# move left
				tempx = piece.x + 1
    				while tempx > -1 and tempx < 8
    					# move into empty space
    					if self.board[piece.y][tempx] == em :
                            
    					# take enemy peice	
    					elif self.board[piece.y][tempx]: 
	
					

				
				break
			case "q":
			case "Q":
				# move up
				tempy = piece.y - 1
				while ((tempy > -1 and tempy < 8)) 
					# move into empty space
					if (board[tempy][piece.x] == "*") 
						validMoves.add(new Move(piece.x, piece.y, piece.x, tempy, piece.type, "", ""))
						tempy--
					 else 
						# take enemy peice
						if (getPiece(piece.x, tempy).white != piece.white) 
							validMoves.add(new Move(piece.x, piece.y, piece.x, tempy, piece.type, "x", ""))

						
						break
					

				
				# move down
				tempy = piece.y + 1
				while ((tempy > -1 and tempy < 8)) 
					# move into empty space
					if (board[tempy][piece.x] == "*") 
						validMoves.add(new Move(piece.x, piece.y, piece.x, tempy, piece.type, "", ""))
						tempy++
					 else 
						# take enemy peice
						if (getPiece(piece.x, tempy).white != piece.white) 
							validMoves.add(new Move(piece.x, piece.y, piece.x, tempy, piece.type, "x", ""))

						
						break
					

				
				# move right
				tempx = piece.x + 1
				while ((tempx > -1 and tempx < 8)) 
					# move into empty space
					if (board[piece.y][tempx] == "*") 
						validMoves.add(new Move(piece.x, piece.y, tempx, piece.y, piece.type, "", ""))
						tempx++
					 else 
						# take enemy peice
						if (getPiece(tempx, piece.y).white != piece.white) 
							validMoves.add(new Move(piece.x, piece.y, tempx, piece.y, piece.type, "x", ""))

						
						break
					

				
				# move left
				tempx = piece.x - 1
				while ((tempx > -1 and tempx < 8)) 
					# move into empty space
					if (board[piece.y][tempx] == "*") 
						validMoves.add(new Move(piece.x, piece.y, tempx, piece.y, piece.type, "", ""))
						tempx--
					 else 
						# take enemy piece
						if (getPiece(tempx, piece.y).white != piece.white) 
							validMoves.add(new Move(piece.x, piece.y, tempx, piece.y, piece.type, "x", ""))

						
						break
					

				
				# move nw
				tempx = piece.x - 1
				tempy = piece.y - 1
				# if the x,y are within the board
				while ((tempx > -1 and tempx < 8) and (tempy > -1 and tempy < 8)) 
					# if the space is empty
					if (board[tempy][tempx] == "*") 
						validMoves.add(new Move(piece.x, piece.y, tempx, tempy, piece.type, "", ""))
						tempx--
						tempy--
					 else 
						# if their color does not match
						if (getPiece(tempx, tempy).white != piece.white) 
							validMoves.add(new Move(piece.x, piece.y, tempx, tempy, piece.type, "x", ""))

						
						break
					

				
				# move sw
				tempx = piece.x - 1
				tempy = piece.y + 1
				while ((tempx > -1 and tempx < 8) and (tempy > -1 and tempy < 8)) 
					# if the space is empty
					if (board[tempy][tempx] == "*") 
						validMoves.add(new Move(piece.x, piece.y, tempx, tempy, piece.type, "", ""))
						tempx--
						tempy++
					 else 
						# if their color does not match
						if (getPiece(tempx, tempy).white != piece.white) 
							validMoves.add(new Move(piece.x, piece.y, tempx, tempy, piece.type, "x", ""))

						
						break
					
				

				# move ne
				tempx = piece.x + 1
				tempy = piece.y - 1
				while ((tempx > -1 and tempx < 8) and (tempy > -1 and tempy < 8)) 
					# if the space is empty
					if (board[tempy][tempx] == "*") 
						validMoves.add(new Move(piece.x, piece.y, tempx, tempy, piece.type, "", ""))
						tempx++
						tempy--
					 else 
						# if their color does not match
						if (getPiece(tempx, tempy).white != piece.white) 
							validMoves.add(new Move(piece.x, piece.y, tempx, tempy, piece.type, "x", ""))
						
						break
					

				
				# move se
				tempx = piece.x + 1
				tempy = piece.y + 1
				while ((tempx > -1 and tempx < 8) and (tempy > -1 and tempy < 8)) 
					# if the space is empty
					if (board[tempy][tempx] == "*") 
						validMoves.add(new Move(piece.x, piece.y, tempx, tempy, piece.type, "", ""))
						tempx++
						tempy++
					 else 
						# if their color does not match
						if (getPiece(tempx, tempy).white != piece.white) 
							validMoves.add(new Move(piece.x, piece.y, tempx, tempy, piece.type, "x", ""))
						
						break
					

				
				break
			case "N":
			case "n":
				# north jump, left
				tempx = (piece.x - 1)
				tempy = (piece.y - 2)
				if ((tempx > -1 and tempx < 8) and (tempy > -1 and tempy < 8)) 
					if (board[tempy][tempx] == "*") 
						validMoves.add(new Move(piece.x, piece.y, tempx, tempy, piece.type, "", ""))
					 else if (getPiece(tempx, tempy).white != piece.white) 
						validMoves.add(new Move(piece.x, piece.y, tempx, tempy, piece.type, "x", ""))
					
				
				# north jump, right
				tempx = (piece.x + 1)
				tempy = (piece.y - 2)
				if ((tempx > -1 and tempx < 8) and (tempy > -1 and tempy < 8)) 
					if (board[tempy][tempx] == "*") 
						validMoves.add(new Move(piece.x, piece.y, tempx, tempy, piece.type, "", ""))
					 else if (getPiece(tempx, tempy).white != piece.white) 
						validMoves.add(new Move(piece.x, piece.y, tempx, tempy, piece.type, "x", ""))
					
				
				# south jump, left
				tempx = (piece.x - 1)
				tempy = (piece.y + 2)
				if ((tempx > -1 and tempx < 8) and (tempy > -1 and tempy < 8)) 
					if (board[tempy][tempx] == "*") 
						validMoves.add(new Move(piece.x, piece.y, tempx, tempy, piece.type, "", ""))
					 else if (getPiece(tempx, tempy).white != piece.white) 
						validMoves.add(new Move(piece.x, piece.y, tempx, tempy, piece.type, "x", ""))
					
				
				# south jump, right
				tempx = (piece.x + 1)
				tempy = (piece.y + 2)
				if ((tempx > -1 and tempx < 8) and (tempy > -1 and tempy < 8)) 
					if (board[tempy][tempx] == "*") 
						validMoves.add(new Move(piece.x, piece.y, tempx, tempy, piece.type, "", ""))
					 else if (getPiece(tempx, tempy).white != piece.white) 
						validMoves.add(new Move(piece.x, piece.y, tempx, tempy, piece.type, "x", ""))
					
				
				# west jump, up
				tempx = (piece.x - 2)
				tempy = (piece.y - 1)
				if ((tempx > -1 and tempx < 8) and (tempy > -1 and tempy < 8)) 
					if (board[tempy][tempx] == "*") 
						validMoves.add(new Move(piece.x, piece.y, tempx, tempy, piece.type, "", ""))
					 else if (getPiece(tempx, tempy).white != piece.white) 
						validMoves.add(new Move(piece.x, piece.y, tempx, tempy, piece.type, "x", ""))
					
				
				# west jump, down
				tempx = (piece.x - 2)
				tempy = (piece.y + 1)
				if ((tempx > -1 and tempx < 8) and (tempy > -1 and tempy < 8)) 
					if (board[tempy][tempx] == "*") 
						validMoves.add(new Move(piece.x, piece.y, tempx, tempy, piece.type, "", ""))
					 else if (getPiece(tempx, tempy).white != piece.white) 
						validMoves.add(new Move(piece.x, piece.y, tempx, tempy, piece.type, "x", ""))
					
				
				# east jump, up
				tempx = (piece.x + 2)
				tempy = (piece.y - 1)
				if ((tempx > -1 and tempx < 8) and (tempy > -1 and tempy < 8)) 
					if (board[tempy][tempx] == "*") 
						validMoves.add(new Move(piece.x, piece.y, tempx, tempy, piece.type, "", ""))
					 else if (getPiece(tempx, tempy).white != piece.white) 
						validMoves.add(new Move(piece.x, piece.y, tempx, tempy, piece.type, "x", ""))
					
				
				# east jump, down
				tempx = (piece.x + 2)
				tempy = (piece.y + 1)
				if ((tempx > -1 and tempx < 8) and (tempy > -1 and tempy < 8)) 
					if (board[tempy][tempx] == "*") 
						validMoves.add(new Move(piece.x, piece.y, tempx, tempy, piece.type, "", ""))
					 else if (getPiece(tempx, tempy).white != piece.white) 
						validMoves.add(new Move(piece.x, piece.y, tempx, tempy, piece.type, "x", ""))
					
				
				break
			case "k":
			case "K":

				# up
				tempx = piece.x
				tempy = piece.y - 1
				if ((tempx > -1 and tempx < 8) and (tempy > -1 and tempy < 8)) 
					if (board[tempy][tempx] == "*") 
						validMoves.add(new Move(piece.x, piece.y, tempx, tempy, piece.type, "", ""))
					 else if (getPiece(tempx, tempy).white != piece.white) 
						validMoves.add(new Move(piece.x, piece.y, tempx, tempy, piece.type, "x", ""))
					
				
				# nw
				tempx = piece.x - 1
				tempy = piece.y - 1
				if ((tempx > -1 and tempx < 8) and (tempy > -1 and tempy < 8)) 
					if (board[tempy][tempx] == "*") 
						validMoves.add(new Move(piece.x, piece.y, tempx, tempy, piece.type, "", ""))
					 else if (getPiece(tempx, tempy).white != piece.white) 
						validMoves.add(new Move(piece.x, piece.y, tempx, tempy, piece.type, "x", ""))
					
				
				# ne
				tempx = piece.x + 1
				tempy = piece.y - 1
				if ((tempx > -1 and tempx < 8) and (tempy > -1 and tempy < 8)) 
					if (board[tempy][tempx] == "*") 
						validMoves.add(new Move(piece.x, piece.y, tempx, tempy, piece.type, "", ""))
					 else if (getPiece(tempx, tempy).white != piece.white) 
						validMoves.add(new Move(piece.x, piece.y, tempx, tempy, piece.type, "x", ""))
					
				
				# w
				tempx = piece.x - 1
				tempy = piece.y
				if ((tempx > -1 and tempx < 8) and (tempy > -1 and tempy < 8)) 
					if (board[tempy][tempx] == "*") 
						validMoves.add(new Move(piece.x, piece.y, tempx, tempy, piece.type, "", ""))
					 else if (getPiece(tempx, tempy).white != piece.white) 
						validMoves.add(new Move(piece.x, piece.y, tempx, tempy, piece.type, "x", ""))
					
				
				# e
				tempx = piece.x - 1
				tempy = piece.y
				if ((tempx > -1 and tempx < 8) and (tempy > -1 and tempy < 8)) 
					if (board[tempy][tempx] == "*") 
						validMoves.add(new Move(piece.x, piece.y, tempx, tempy, piece.type, "", ""))
					 else if (getPiece(tempx, tempy).white != piece.white) 
						validMoves.add(new Move(piece.x, piece.y, tempx, tempy, piece.type, "x", ""))
					
				
				# s
				tempx = piece.x
				tempy = piece.y + 1
				if ((tempx > -1 and tempx < 8) and (tempy > -1 and tempy < 8)) 
					if (board[tempy][tempx] == "*") 
						validMoves.add(new Move(piece.x, piece.y, tempx, tempy, piece.type, "", ""))
					 else if (getPiece(tempx, tempy).white != piece.white) 
						validMoves.add(new Move(piece.x, piece.y, tempx, tempy, piece.type, "x", ""))
					
				
				# sw
				tempx = piece.x - 1
				tempy = piece.y - 1
				if ((tempx > -1 and tempx < 8) and (tempy > -1 and tempy < 8)) 
					if (board[tempy][tempx] == "*") 
						validMoves.add(new Move(piece.x, piece.y, tempx, tempy, piece.type, "", ""))
					 else if (getPiece(tempx, tempy).white != piece.white) 
						validMoves.add(new Move(piece.x, piece.y, tempx, tempy, piece.type, "x", ""))
					
				
				# se
				tempx = piece.x + 1
				tempy = piece.y + 1
				if ((tempx > -1 and tempx < 8) and (tempy > -1 and tempy < 8)) 
					if (board[tempy][tempx] == "*") 
						validMoves.add(new Move(piece.x, piece.y, tempx, tempy, piece.type, "", ""))
					 else if (getPiece(tempx, tempy).white != piece.white) 
						validMoves.add(new Move(piece.x, piece.y, tempx, tempy, piece.type, "x", ""))
					
				
                """
        

   
    def __str__(self):
        return str(self.board)+"\n"+str(self.turnNum)
    
    def setup_vanilla(self):
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