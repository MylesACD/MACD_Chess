import Move as m
import Piece as p
import State as s

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


move = m.Move(wk,0,0,0,1,"")
game_state = s.State()
game_state.setup_vanilla()

print(game_state)
