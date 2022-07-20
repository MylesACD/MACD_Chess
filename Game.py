import Move as m
import Piece as p
import State as s
import Agents as a
import time
import numpy as np
import random
import PGN_To_Boards as ptb
import pickle
import threading as thd
import concurrent


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
black = 0
white = 1

#------------------gobal variables for testing--------------------------------


#-----------------------------------------------------------------------------


    
class normal_game:
    
    def __init__(self, wplayer,bplayer, turn_limit = np.inf):
        self.game_state = s.State()
        self.game_state.setup_vanilla()
        self.players = [bplayer,wplayer]
        self.turn_num = 1
        self.moves_played = []
        self.turn_limit = turn_limit
        
    def set_white_player(self, player):
        self.players[1] = player
    
    def set_black_player(self, player):
        self.playres[0] = player
    
    def __str__(self):
        return str(self.game_state)
    
    def print_PGN(self):
        output = "\n"
        for move in self.moves_played:
            output += move +"\n"
        print(output)
        
    def next_turn(self):
        move = self.players[self.turn_num%2].choose_move(self.game_state)
        self.moves_played.append(str(move))
        self.game_state = self.game_state.generateSuccessor(move)
        self.turn_num +=1
        
    def is_over(self):
        return self.game_state.is_terminal() or self.turn_num > self.turn_limit
    
    def run(self):
        while not self.is_over():
            game.next_turn()
        return self.game_state.standard_mat_eval(white)

    
    
if __name__=="__main__":
#--------------------Testing stuff-----------------------
    whitePlayer = a.minimax_agent(3,white)
    blackPlayer = a.minimax_agent(3,black)

    results =[]
    noG  = 1
    length =50
    start = time.perf_counter()
    try:
        for i in range(noG):
            game = normal_game(whitePlayer,blackPlayer,length)
            game.run()
            game.print_PGN()
    except:
        game.print_PGN()
        print("----------ERROR----------")
    total_time = time.perf_counter()-start
    print("Seconds per turn: ",round((total_time)/noG/length,2))
    
    '''
    times = s.get_op_stats()
    for key,value in times.items():
        print(key,": " ,round(100*value/total_time,3))
    '''
  
#--------------------------------------------------------------

    
    
