import Move as m
import Piece as p
import State as s
import time
import numpy as np
import random
import PGN_To_Boards as ptb
import pickle
import threading as thd


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

#whatever game type is being played the real gamestate must be created

def random_move(state):
    valid_moves = state.generate_all_moves()
    x= random.randint(0, len(valid_moves)-1)
    return valid_moves[x]
    
#
def mmm_helper(state,color,target_depth,a,b,is_maxing):
    results.append(mat_minimax(state, color, target_depth, a, b, is_maxing))

# returns the max move for that player 
def mat_minimax(state, color, target_depth, a, b, is_maxing):
    # this might be a significant performance hit
    temp_state = state
  
    
    # checks if the state is terminal
   
    if target_depth==0 or state.is_terminal():
        return temp_state.standard_mat_eval(color)
    
    elif is_maxing:
        child_states = temp_state.generate_all_successor_states()
        value = -1000
        for child in child_states:
            value = max(value, mat_minimax(child, color,target_depth-1, a, b,False))
            a = max(a, value)
            if value >= b:
                break
        return value
    else:
        child_states = temp_state.generate_all_successor_states()
        value = 1000
        for child in child_states:
            value = min(value, mat_minimax(child,color, target_depth-1, a, b, True))
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
    
class minimax_agent(agent):
    def __init__(self, depth, color):
        self.play_func = mmm_helper
        self.depth = depth
        self.color = color
        
    def choose_move(self, state):
        # 0 depth means no evaluation of future nodes, so choose one at random
        if self.depth <1:
            return random_move(state)
            
        moves = state.generate_all_moves()
        # saving time by not recalculating all moves
        states = [state.generateSuccessor(move) for move in moves]
        # run minimax on all of the future states
       
        # expiramental using multiprocessing
        global results
        results = []
        threads = [thd.Thread(target=mmm_helper, args=(future_state, self.color,self.depth-1, -1000,1000,False)) for future_state in states]
        [thread.start() for thread in threads]
        [thread.join() for thread in threads]
   
        #results = [self.play_func(future_state, self.color,self.depth-1, -1000,1000,False) for future_state in states]
       
        best = max(results)
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
        self.turn_num = 0
        self.moves_played = []
        self.turn_limit = turn_limit
        
    def set_white_player(self, player):
        self.players[1] = player
    
    def set_black_player(self, player):
        self.playres[0] = player
    
    def __str__(self):
        return str(self.moves_played)
    
    def print_PGN(self):
        output = "\n"
        for move in self.moves_played:
            output += move +"\n"
        print(output)
        
    def next_turn(self):
        self.turn_num +=1
        move = self.players[self.turn_num%2].choose_move(self.game_state)
        self.moves_played.append(str(move))
        self.game_state = self.game_state.generateSuccessor(move)
        
    def is_over(self):
        return self.game_state.is_terminal() or self.turn_num >self.turn_limit

    
    
if __name__=="__main__":
#--------------------Testing stuff-----------------------
    whitePlayer = minimax_agent(3,white)
    blackPlayer = minimax_agent(3,black)
    game = normal_game(whitePlayer,blackPlayer,30)
    #model = pickle.load(open("300forest.sav", 'rb'))
    #print(model.predict_proba([game.game_state.convert_board_to_num(True)]))
    times = []
    while not game.is_over():
        t = time.perf_counter()
        game.next_turn()
        game.next_turn()
     #  print(model.predict_proba([game.game_state.convert_board_to_num(True)]))
        dur = time.perf_counter()-t
        print(dur)
        times.append(dur)
    
    game.print_PGN()
    print("AVG: ",np.average(times))
    
    #print(game_state.convert_board_to_num())

#--------------------------------------------------------------
    
