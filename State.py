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
                
        
        switch (piece.type) {
			// white pawn
			case "P":

				// move 1 forward
				if (board[piece.y - 1][piece.x] == "*")
					validMoves.add(new Move(piece.x, piece.y, piece.x, piece.y - 1, piece.type, "", ""));
				// move 2 forward
				if (piece.y == 6 && board[piece.y - 2][piece.x] == "*" && board[piece.y - 1][piece.x] == "*")
					validMoves.add(new Move(piece.x, piece.y, piece.x, piece.y - 2, piece.type, "", ""));
				// take left
				if (piece.x != 0 && piece.y != 0 && board[piece.y - 1][piece.x - 1] != "*"
						&& board[piece.y - 1][piece.x - 1].toLowerCase() == board[piece.y - 1][piece.x - 1])
					validMoves.add(new Move(piece.x, piece.y, piece.x - 1, piece.y - 1, piece.type, "x", ""));
				// take right
				if (piece.x != 7 && board[piece.y - 1][piece.x + 1] != "*"
						&& board[piece.y - 1][piece.x + 1].toLowerCase() == board[piece.y - 1][piece.x + 1])
					validMoves.add(new Move(piece.x, piece.y, piece.x + 1, piece.y - 1, piece.type, "x", ""));
				// en passant
				if (previous != null && piece.y == 5 && previous.piece == "o" && previous.ey - previous.sy == 2
						&& (previous.ex == piece.x - 1 || previous.ex == piece.x + 1)) {
					validMoves.add(new Move(piece.x, piece.y, previous.ex, previous.ey - 1, piece.type, "x", ""));
				}
				break;
			// black pawn
			case "o":
				// move 1 forward
				if (board[piece.y + 1][piece.x] == "*")
					validMoves.add(new Move(piece.x, piece.y, piece.x, piece.y + 1, piece.type, "", ""));
				// move 2 forward
				if (piece.y == 1 && board[piece.y + 2][piece.x] == "*" && board[piece.y + 1][piece.x] == "*")
					validMoves.add(new Move(piece.x, piece.y, piece.x, piece.y + 2, piece.type, "", ""));
				// take left
				if (piece.x != 0 && board[piece.y + 1][piece.x - 1] != "*"
						&& board[piece.y + 1][piece.x - 1].toUpperCase() == board[piece.y + 1][piece.x - 1])
					validMoves.add(new Move(piece.x, piece.y, piece.x - 1, piece.y + 1, piece.type, "x", ""));
				// take right
				if (piece.x != 7 && board[piece.y + 1][piece.x + 1] != "*"
						&& board[piece.y + 1][piece.x + 1].toUpperCase() == board[piece.y + 1][piece.x + 1])
					validMoves.add(new Move(piece.x, piece.y, piece.x + 1, piece.y + 1, piece.type, "x", ""));
				// en passant
				if (previous != null && piece.y == 4 && previous.piece == "P" && previous.ey - previous.sy == -2
						&& (previous.ex == piece.x - 1 || previous.ex == piece.x + 1)) {
					validMoves.add(new Move(piece.x, piece.y, previous.ex, previous.ey + 1, piece.type, "x", ""));
				}
				break;

			case "B":
			case "b":
				// move nw
				int tempx = piece.x - 1;
				int tempy = piece.y - 1;
				// if the x,y are within the board
				while ((tempx > -1 && tempx < 8) && (tempy > -1 && tempy < 8)) {
					// if the space is empty
					if (board[tempy][tempx] == "*") {
						validMoves.add(new Move(piece.x, piece.y, tempx, tempy, piece.type, "", ""));
						tempx--;
						tempy--;
					} else {
						// if their color does not match
						if (getPiece(tempx, tempy).white != piece.white) {
							validMoves.add(new Move(piece.x, piece.y, tempx, tempy, piece.type, "x", ""));

						}
						break;
					}

				}
				// move sw
				tempx = piece.x - 1;
				tempy = piece.y + 1;
				while ((tempx > -1 && tempx < 8) && (tempy > -1 && tempy < 8)) {
					// if the space is empty
					if (board[tempy][tempx] == "*") {
						validMoves.add(new Move(piece.x, piece.y, tempx, tempy, piece.type, "", ""));
						tempx--;
						tempy++;
					} else {
						// if their color does not match
						if (getPiece(tempx, tempy).white != piece.white) {
							validMoves.add(new Move(piece.x, piece.y, tempx, tempy, piece.type, "x", ""));

						}
						break;
					}
				}

				// move ne
				tempx = piece.x + 1;
				tempy = piece.y - 1;
				while ((tempx > -1 && tempx < 8) && (tempy > -1 && tempy < 8)) {
					// if the space is empty
					if (board[tempy][tempx] == "*") {
						validMoves.add(new Move(piece.x, piece.y, tempx, tempy, piece.type, "", ""));
						tempx++;
						tempy--;
					} else {
						// if their color does not match
						if (getPiece(tempx, tempy).white != piece.white) {
							validMoves.add(new Move(piece.x, piece.y, tempx, tempy, piece.type, "x", ""));
						}
						break;
					}

				}
				// move se
				tempx = piece.x + 1;
				tempy = piece.y + 1;
				while ((tempx > -1 && tempx < 8) && (tempy > -1 && tempy < 8)) {
					// if the space is empty
					if (board[tempy][tempx] == "*") {
						validMoves.add(new Move(piece.x, piece.y, tempx, tempy, piece.type, "", ""));
						tempx++;
						tempy++;
					} else {
						// if their color does not match
						if (getPiece(tempx, tempy).white != piece.white) {
							validMoves.add(new Move(piece.x, piece.y, tempx, tempy, piece.type, "x", ""));
						}
						break;
					}

				}
				break;

			case "r":
			case "R":
				// move up
				tempy = piece.y - 1;
				while ((tempy > -1 && tempy < 8)) {
					// move into empty space
					if (board[tempy][piece.x] == "*") {
						validMoves.add(new Move(piece.x, piece.y, piece.x, tempy, piece.type, "", ""));
						tempy--;
					} else {
						// take enemy peice
						if (getPiece(piece.x, tempy).white != piece.white) {
							validMoves.add(new Move(piece.x, piece.y, piece.x, tempy, piece.type, "x", ""));

						}
						break;
					}

				}
				// move down
				tempy = piece.y + 1;
				while ((tempy > -1 && tempy < 8)) {
					// move into empty space
					if (board[tempy][piece.x] == "*") {
						validMoves.add(new Move(piece.x, piece.y, piece.x, tempy, piece.type, "", ""));
						tempy++;
					} else {
						// take enemy peice
						if (getPiece(piece.x, tempy).white != piece.white) {
							validMoves.add(new Move(piece.x, piece.y, piece.x, tempy, piece.type, "x", ""));

						}
						break;
					}

				}
				// move right
				tempx = piece.x + 1;
				while ((tempx > -1 && tempx < 8)) {
					// move into empty space
					if (board[piece.y][tempx] == "*") {
						validMoves.add(new Move(piece.x, piece.y, tempx, piece.y, piece.type, "", ""));
						tempx++;
					} else {
						// take enemy peice
						if (getPiece(tempx, piece.y).white != piece.white) {
							validMoves.add(new Move(piece.x, piece.y, tempx, piece.y, piece.type, "x", ""));

						}
						break;
					}

				}
				// move left
				tempx = piece.x - 1;
				while ((tempx > -1 && tempx < 8)) {
					// move into empty space
					if (board[piece.y][tempx] == "*") {
						validMoves.add(new Move(piece.x, piece.y, tempx, piece.y, piece.type, "", ""));
						tempx--;
					} else {
						// take enemy piece
						if (getPiece(tempx, piece.y).white != piece.white) {
							validMoves.add(new Move(piece.x, piece.y, tempx, piece.y, piece.type, "x", ""));

						}
						break;
					}

				}
				break;
			case "q":
			case "Q":
				// move up
				tempy = piece.y - 1;
				while ((tempy > -1 && tempy < 8)) {
					// move into empty space
					if (board[tempy][piece.x] == "*") {
						validMoves.add(new Move(piece.x, piece.y, piece.x, tempy, piece.type, "", ""));
						tempy--;
					} else {
						// take enemy peice
						if (getPiece(piece.x, tempy).white != piece.white) {
							validMoves.add(new Move(piece.x, piece.y, piece.x, tempy, piece.type, "x", ""));

						}
						break;
					}

				}
				// move down
				tempy = piece.y + 1;
				while ((tempy > -1 && tempy < 8)) {
					// move into empty space
					if (board[tempy][piece.x] == "*") {
						validMoves.add(new Move(piece.x, piece.y, piece.x, tempy, piece.type, "", ""));
						tempy++;
					} else {
						// take enemy peice
						if (getPiece(piece.x, tempy).white != piece.white) {
							validMoves.add(new Move(piece.x, piece.y, piece.x, tempy, piece.type, "x", ""));

						}
						break;
					}

				}
				// move right
				tempx = piece.x + 1;
				while ((tempx > -1 && tempx < 8)) {
					// move into empty space
					if (board[piece.y][tempx] == "*") {
						validMoves.add(new Move(piece.x, piece.y, tempx, piece.y, piece.type, "", ""));
						tempx++;
					} else {
						// take enemy peice
						if (getPiece(tempx, piece.y).white != piece.white) {
							validMoves.add(new Move(piece.x, piece.y, tempx, piece.y, piece.type, "x", ""));

						}
						break;
					}

				}
				// move left
				tempx = piece.x - 1;
				while ((tempx > -1 && tempx < 8)) {
					// move into empty space
					if (board[piece.y][tempx] == "*") {
						validMoves.add(new Move(piece.x, piece.y, tempx, piece.y, piece.type, "", ""));
						tempx--;
					} else {
						// take enemy piece
						if (getPiece(tempx, piece.y).white != piece.white) {
							validMoves.add(new Move(piece.x, piece.y, tempx, piece.y, piece.type, "x", ""));

						}
						break;
					}

				}
				// move nw
				tempx = piece.x - 1;
				tempy = piece.y - 1;
				// if the x,y are within the board
				while ((tempx > -1 && tempx < 8) && (tempy > -1 && tempy < 8)) {
					// if the space is empty
					if (board[tempy][tempx] == "*") {
						validMoves.add(new Move(piece.x, piece.y, tempx, tempy, piece.type, "", ""));
						tempx--;
						tempy--;
					} else {
						// if their color does not match
						if (getPiece(tempx, tempy).white != piece.white) {
							validMoves.add(new Move(piece.x, piece.y, tempx, tempy, piece.type, "x", ""));

						}
						break;
					}

				}
				// move sw
				tempx = piece.x - 1;
				tempy = piece.y + 1;
				while ((tempx > -1 && tempx < 8) && (tempy > -1 && tempy < 8)) {
					// if the space is empty
					if (board[tempy][tempx] == "*") {
						validMoves.add(new Move(piece.x, piece.y, tempx, tempy, piece.type, "", ""));
						tempx--;
						tempy++;
					} else {
						// if their color does not match
						if (getPiece(tempx, tempy).white != piece.white) {
							validMoves.add(new Move(piece.x, piece.y, tempx, tempy, piece.type, "x", ""));

						}
						break;
					}
				}

				// move ne
				tempx = piece.x + 1;
				tempy = piece.y - 1;
				while ((tempx > -1 && tempx < 8) && (tempy > -1 && tempy < 8)) {
					// if the space is empty
					if (board[tempy][tempx] == "*") {
						validMoves.add(new Move(piece.x, piece.y, tempx, tempy, piece.type, "", ""));
						tempx++;
						tempy--;
					} else {
						// if their color does not match
						if (getPiece(tempx, tempy).white != piece.white) {
							validMoves.add(new Move(piece.x, piece.y, tempx, tempy, piece.type, "x", ""));
						}
						break;
					}

				}
				// move se
				tempx = piece.x + 1;
				tempy = piece.y + 1;
				while ((tempx > -1 && tempx < 8) && (tempy > -1 && tempy < 8)) {
					// if the space is empty
					if (board[tempy][tempx] == "*") {
						validMoves.add(new Move(piece.x, piece.y, tempx, tempy, piece.type, "", ""));
						tempx++;
						tempy++;
					} else {
						// if their color does not match
						if (getPiece(tempx, tempy).white != piece.white) {
							validMoves.add(new Move(piece.x, piece.y, tempx, tempy, piece.type, "x", ""));
						}
						break;
					}

				}
				break;
			case "N":
			case "n":
				// north jump, left
				tempx = (piece.x - 1);
				tempy = (piece.y - 2);
				if ((tempx > -1 && tempx < 8) && (tempy > -1 && tempy < 8)) {
					if (board[tempy][tempx] == "*") {
						validMoves.add(new Move(piece.x, piece.y, tempx, tempy, piece.type, "", ""));
					} else if (getPiece(tempx, tempy).white != piece.white) {
						validMoves.add(new Move(piece.x, piece.y, tempx, tempy, piece.type, "x", ""));
					}
				}
				// north jump, right
				tempx = (piece.x + 1);
				tempy = (piece.y - 2);
				if ((tempx > -1 && tempx < 8) && (tempy > -1 && tempy < 8)) {
					if (board[tempy][tempx] == "*") {
						validMoves.add(new Move(piece.x, piece.y, tempx, tempy, piece.type, "", ""));
					} else if (getPiece(tempx, tempy).white != piece.white) {
						validMoves.add(new Move(piece.x, piece.y, tempx, tempy, piece.type, "x", ""));
					}
				}
				// south jump, left
				tempx = (piece.x - 1);
				tempy = (piece.y + 2);
				if ((tempx > -1 && tempx < 8) && (tempy > -1 && tempy < 8)) {
					if (board[tempy][tempx] == "*") {
						validMoves.add(new Move(piece.x, piece.y, tempx, tempy, piece.type, "", ""));
					} else if (getPiece(tempx, tempy).white != piece.white) {
						validMoves.add(new Move(piece.x, piece.y, tempx, tempy, piece.type, "x", ""));
					}
				}
				// south jump, right
				tempx = (piece.x + 1);
				tempy = (piece.y + 2);
				if ((tempx > -1 && tempx < 8) && (tempy > -1 && tempy < 8)) {
					if (board[tempy][tempx] == "*") {
						validMoves.add(new Move(piece.x, piece.y, tempx, tempy, piece.type, "", ""));
					} else if (getPiece(tempx, tempy).white != piece.white) {
						validMoves.add(new Move(piece.x, piece.y, tempx, tempy, piece.type, "x", ""));
					}
				}
				// west jump, up
				tempx = (piece.x - 2);
				tempy = (piece.y - 1);
				if ((tempx > -1 && tempx < 8) && (tempy > -1 && tempy < 8)) {
					if (board[tempy][tempx] == "*") {
						validMoves.add(new Move(piece.x, piece.y, tempx, tempy, piece.type, "", ""));
					} else if (getPiece(tempx, tempy).white != piece.white) {
						validMoves.add(new Move(piece.x, piece.y, tempx, tempy, piece.type, "x", ""));
					}
				}
				// west jump, down
				tempx = (piece.x - 2);
				tempy = (piece.y + 1);
				if ((tempx > -1 && tempx < 8) && (tempy > -1 && tempy < 8)) {
					if (board[tempy][tempx] == "*") {
						validMoves.add(new Move(piece.x, piece.y, tempx, tempy, piece.type, "", ""));
					} else if (getPiece(tempx, tempy).white != piece.white) {
						validMoves.add(new Move(piece.x, piece.y, tempx, tempy, piece.type, "x", ""));
					}
				}
				// east jump, up
				tempx = (piece.x + 2);
				tempy = (piece.y - 1);
				if ((tempx > -1 && tempx < 8) && (tempy > -1 && tempy < 8)) {
					if (board[tempy][tempx] == "*") {
						validMoves.add(new Move(piece.x, piece.y, tempx, tempy, piece.type, "", ""));
					} else if (getPiece(tempx, tempy).white != piece.white) {
						validMoves.add(new Move(piece.x, piece.y, tempx, tempy, piece.type, "x", ""));
					}
				}
				// east jump, down
				tempx = (piece.x + 2);
				tempy = (piece.y + 1);
				if ((tempx > -1 && tempx < 8) && (tempy > -1 && tempy < 8)) {
					if (board[tempy][tempx] == "*") {
						validMoves.add(new Move(piece.x, piece.y, tempx, tempy, piece.type, "", ""));
					} else if (getPiece(tempx, tempy).white != piece.white) {
						validMoves.add(new Move(piece.x, piece.y, tempx, tempy, piece.type, "x", ""));
					}
				}
				break;
			case "k":
			case "K":

				// up
				tempx = piece.x;
				tempy = piece.y - 1;
				if ((tempx > -1 && tempx < 8) && (tempy > -1 && tempy < 8)) {
					if (board[tempy][tempx] == "*") {
						validMoves.add(new Move(piece.x, piece.y, tempx, tempy, piece.type, "", ""));
					} else if (getPiece(tempx, tempy).white != piece.white) {
						validMoves.add(new Move(piece.x, piece.y, tempx, tempy, piece.type, "x", ""));
					}
				}
				// nw
				tempx = piece.x - 1;
				tempy = piece.y - 1;
				if ((tempx > -1 && tempx < 8) && (tempy > -1 && tempy < 8)) {
					if (board[tempy][tempx] == "*") {
						validMoves.add(new Move(piece.x, piece.y, tempx, tempy, piece.type, "", ""));
					} else if (getPiece(tempx, tempy).white != piece.white) {
						validMoves.add(new Move(piece.x, piece.y, tempx, tempy, piece.type, "x", ""));
					}
				}
				// ne
				tempx = piece.x + 1;
				tempy = piece.y - 1;
				if ((tempx > -1 && tempx < 8) && (tempy > -1 && tempy < 8)) {
					if (board[tempy][tempx] == "*") {
						validMoves.add(new Move(piece.x, piece.y, tempx, tempy, piece.type, "", ""));
					} else if (getPiece(tempx, tempy).white != piece.white) {
						validMoves.add(new Move(piece.x, piece.y, tempx, tempy, piece.type, "x", ""));
					}
				}
				// w
				tempx = piece.x - 1;
				tempy = piece.y;
				if ((tempx > -1 && tempx < 8) && (tempy > -1 && tempy < 8)) {
					if (board[tempy][tempx] == "*") {
						validMoves.add(new Move(piece.x, piece.y, tempx, tempy, piece.type, "", ""));
					} else if (getPiece(tempx, tempy).white != piece.white) {
						validMoves.add(new Move(piece.x, piece.y, tempx, tempy, piece.type, "x", ""));
					}
				}
				// e
				tempx = piece.x - 1;
				tempy = piece.y;
				if ((tempx > -1 && tempx < 8) && (tempy > -1 && tempy < 8)) {
					if (board[tempy][tempx] == "*") {
						validMoves.add(new Move(piece.x, piece.y, tempx, tempy, piece.type, "", ""));
					} else if (getPiece(tempx, tempy).white != piece.white) {
						validMoves.add(new Move(piece.x, piece.y, tempx, tempy, piece.type, "x", ""));
					}
				}
				// s
				tempx = piece.x;
				tempy = piece.y + 1;
				if ((tempx > -1 && tempx < 8) && (tempy > -1 && tempy < 8)) {
					if (board[tempy][tempx] == "*") {
						validMoves.add(new Move(piece.x, piece.y, tempx, tempy, piece.type, "", ""));
					} else if (getPiece(tempx, tempy).white != piece.white) {
						validMoves.add(new Move(piece.x, piece.y, tempx, tempy, piece.type, "x", ""));
					}
				}
				// sw
				tempx = piece.x - 1;
				tempy = piece.y - 1;
				if ((tempx > -1 && tempx < 8) && (tempy > -1 && tempy < 8)) {
					if (board[tempy][tempx] == "*") {
						validMoves.add(new Move(piece.x, piece.y, tempx, tempy, piece.type, "", ""));
					} else if (getPiece(tempx, tempy).white != piece.white) {
						validMoves.add(new Move(piece.x, piece.y, tempx, tempy, piece.type, "x", ""));
					}
				}
				// se
				tempx = piece.x + 1;
				tempy = piece.y + 1;
				if ((tempx > -1 && tempx < 8) && (tempy > -1 && tempy < 8)) {
					if (board[tempy][tempx] == "*") {
						validMoves.add(new Move(piece.x, piece.y, tempx, tempy, piece.type, "", ""));
					} else if (getPiece(tempx, tempy).white != piece.white) {
						validMoves.add(new Move(piece.x, piece.y, tempx, tempy, piece.type, "x", ""));
					}
				}

			}
   
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
        
        for (int i = 0; i < 8; i++) {
			blackPieces.add(new Piece("o", i, 1, 1, false));
			whitePieces.add(new Piece("P", i, 6, 1, true));
		}
		blackPieces.add(new Piece("r", 0, 0, 6, false));
		blackPieces.add(new Piece("n", 1, 0, 3, false));
		blackPieces.add(new Piece("b", 2, 0, 3, false));
		blackPieces.add(new Piece("q", 3, 0, 9, false));
		blackPieces.add(new Piece("k", 4, 0, 100, false));
		blackPieces.add(new Piece("b", 5, 0, 3, false));
		blackPieces.add(new Piece("n", 6, 0, 3, false));
		blackPieces.add(new Piece("r", 7, 0, 6, false));

		whitePieces.add(new Piece("R", 0, 7, 6, true));
		whitePieces.add(new Piece("N", 1, 7, 3, true));
		whitePieces.add(new Piece("B", 2, 7, 3, true));
		whitePieces.add(new Piece("Q", 3, 7, 9, true));
		whitePieces.add(new Piece("K", 4, 7, 100, true));
		whitePieces.add(new Piece("B", 5, 7, 3, true));
		whitePieces.add(new Piece("N", 6, 7, 3, true));
		whitePieces.add(new Piece("R", 7, 7, 6, true));
        
        
  