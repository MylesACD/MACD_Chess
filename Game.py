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
        
    def append_to_training(self):
        training = open("evolution_training.txt","w",encoding="utf-8") 
        # tests if the game has a conclusive outcome
        if self.game_state.is_terminal():
            line = ptb.string_rep(self.game_state.convert_board_to_num_array(mat=True))
            training.write(line)
            
        
    def next_turn(self):
        move = self.players[self.turn_num%2].choose_move(self.game_state)
        self.moves_played.append(str(move))
        self.game_state = self.game_state.generateSuccessor(move)
        self.turn_num +=1
        print(str(move))
        
    def is_over(self):
        return self.game_state.is_terminal() or self.turn_num > self.turn_limit
    
    def run(self):
        while not self.is_over():
            game.next_turn()
        self.append_to_training()
        return self.game_state.standard_mat_eval(white)

    
    
if __name__=="__main__":
#--------------------Testing stuff-----------------------
    whitePlayer = a.minimax_agent(3,white)
    blackPlayer = a.minimax_agent(1,black)

    results =[]
    number_of_games  = 1
    length =50
    start = time.perf_counter()
    
    try:
        for i in range(number_of_games):
            game = normal_game(whitePlayer,blackPlayer,length)
            game.run()
    except Exception as inst:
        
        game.print_PGN()
        print("----------ERROR----------")
        print(inst)
        
        
    total_time = time.perf_counter()-start
    print("Seconds per turn: ",round((total_time)/number_of_games/length,2))
    
    '''
    times = s.get_op_stats()
    for key,value in times.items():
        print(key,": " ,round(100*value/total_time,3))
    '''
  
#--------------------------------------------------------------

    
    
