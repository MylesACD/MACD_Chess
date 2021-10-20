import Move as m
import Piece as p
import State as s
import time
import numpy as np
import random

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

#whatever game type is being played the real gamestate must be created
game_state = s.State()
game_state.setup_vanilla()

def time_measure(func):
    start = time.perf_counter()
    rtn = func
    finish = time.perf_counter()
    print(int(finish-start))
    return rtn

def play_random_move():
    global game_state
    valid_moves = game_state.generateMoves()
    x= random.randint(0, len(valid_moves))
    game_state = game_state.generateSuccessor(valid_moves[x])
    

#--------------------Testing stuff-----------------------

play_random_move()


move = m.Move(wp,0,6,"",0,4,"")

print(game_state)

game_state =  time_measure(game_state.generateSuccessor(move))

print(game_state)

#--------------------------------------------------------------
    
