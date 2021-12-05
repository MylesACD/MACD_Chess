import Move as m
import Piece as p
import State as s
import time
import numpy as np
import random
import Collect_Data as cd

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
    print("run time: " + str(int(finish-start)))
    return rtn

def play_random_move(state):
    valid_moves = state.generate_all_moves()
    x= random.randint(0, len(valid_moves)-1)
    print(valid_moves[x])
    state = state.generateSuccessor(valid_moves[x])
    return state
    

#--------------------Testing stuff-----------------------



for i in range(30):
    game_state = play_random_move(game_state)
    print(game_state)

#--------------------------------------------------------------
    
