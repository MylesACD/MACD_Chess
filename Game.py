import Move as m
import Piece as p
import State as s
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

def random_move(state):
    valid_moves = state.generate_all_moves(True)
    x= random.randint(0, len(valid_moves)-1)
    return valid_moves[x]
    
# returns the max or min value for the state
def mat_minimax(state,target_depth, a, b, is_maxing):
    # checks if the state is terminal
    if target_depth<1 or state.is_terminal():
        return state.standard_mat_eval(white)
    
    elif is_maxing:
        child_states = state.generate_all_successor_states()
        value = -1000
        for child in child_states:
            value = max(value, mat_minimax(child,target_depth-1, a, b,False))
            a = max(a, value)
            if value >= b:
                break
        return value
    else:
        child_states = state.generate_all_successor_states()
        value = 1000
        for child in child_states:
            value = min(value, mat_minimax(child, target_depth-1, a, b, True))
            b = min(b, value)
            if value <= a:
                break
        return value

class agent:
    def __init__():
        pass
    def choose_move(self, state):
        return self.play_func(state)
    def prediction():
        pass

class random_agent(agent):
    def __init__(self):
        self.play_func = random_move
    def prediction():
        return 0.5     
    
def human_agent(agent):
    def __init__():
       # self.play_func = humnan_turn 
       pass

class minimax_agent(agent):
    def __init__(self, depth, color):
        self.play_func = mat_minimax
        self.depth = depth
        self.color = color
        if color == black:
            self.other = white
        elif color == white:
            self.other = black
        
    def choose_move(self, state):
        # 0 depth means no evaluation of future nodes, so choose one at random
        if self.depth <1:
            return random_move(state)
            
        moves = state.generate_all_moves(True)
        # saving time by not recalculating all moves
        states = [state.generateSuccessor(move) for move in moves]
        # run minimax on all of the future states
        results=[]
      
        
        # expiramental using multiprocessing
        with concurrent.futures.ProcessPoolExecutor(max_workers=6) as executor:
            if self.color ==white:
                futures = [executor.submit(self.play_func, future_state,self.depth-1, -1000,1000,False) for future_state in states]
            elif self.color == black:
                futures = [executor.submit(self.play_func, future_state,self.depth-1, -1000,1000,True) for future_state in states]

        
            results = [f.result() for f in futures] 
            '''
        # single core processing for debugging and optimization testing
        if self.color==white:
            for state in states:
                results.append(self.play_func(state, self.depth-1, -1000, 1000, False) )
        if self.color==black:
            for state in states:
                 results.append(self.play_func(state, self.depth-1, -1000, 1000, True) )
        '''
        if self.color ==white:
            best = max(results)
        elif self.color == black:
            best = min(results)
       
        indecies=[]
        for i in range(len(results)):
            if results[i]==best:
                indecies.append(i)
        x = random.randint(0, len(indecies)-1)
        return moves[indecies[x]]


    
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
    whitePlayer = minimax_agent(3,white)
    blackPlayer = minimax_agent(3,black)

    results =[]
    noG  = 1
    length =28
    start = time.perf_counter()
   
    for i in range(noG):
        game = normal_game(whitePlayer,blackPlayer,length)
        game.run()
        game.print_PGN()
        #print(game)
    
    print("Seconds per turn: ",round((time.perf_counter()-start)/noG/length,2))

    times = s.get_op_stats()
    for key,value in times.items():
        print(key,": " ,value)
  
#--------------------------------------------------------------

    
    
