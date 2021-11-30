import State as s
import Move as m
import Piece as p


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

boards = []


board = s.State()
board.setup_vanilla()

pgn = "1. e4 e5 2. Nf3 Qf6 3. Bc4 Qg6 4. O-O Qxe4 5. Bxf7+ Kxf7 6. Ng5+ Ke8 7. Nxe4 1-0"

split = pgn.split(" ")

result = split[-1]

moves = [string for string in split if "." not in string]
moves = moves[:-1]

move_text = moves[0]

def gen_board(move_text,board):
    
    


