import State as s
import Move as m
import Piece as p
import numpy as np
import time

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


def gen_board(move_text,state):
  
    if not state:
        return None
    
    move_text = move_text.replace("+","")
    move_text = move_text.replace("#","")
    
    possible_moves = state.generate_all_moves()
    #print("----------------------------")
    for move in possible_moves:
        
        clean1 = move.short().replace("+", "").replace("#", "")
        clean2 = str(move).replace("+", "").replace("#", "")
        clean3 = move.medium1().replace("+", "").replace("#", "")
        clean4 = move.medium2().replace("+", "").replace("#", "")
        # other than checks if the move strings are the same
        if clean1 == move_text or clean2==move_text or clean3==move_text or clean4==move_text:
            return state.generateSuccessor(move)
       
        
    #print("failed for: " , move_text)
    return None


# build the entire series board states of a game
def build_game(game_line):
    split = game_line.split(" ")
    state = s.State()
    state.setup_vanilla()
    result = split[-1]
    moves = [string for string in split if "." not in string]
    moves = moves[:-1]

    boards=[]
    
    for move_text in moves:
        
        state = gen_board(move_text, state)
        if state:
            if state.turnNum>0:
                data_object = state.convert_board_to_num_array(mat=True)
                data_object = np.append(data_object,[result_to_num(result)])
                boards.append(data_object)
        else:
            # the state was unable to be reached so stop trying to process this game_line
            #print("failed for: ",game_line)
            break
    #print(boards[0])
    return boards

def build_sets(num_samples,ratio):
    full = open("PGN Only.txt","r")
    training = open("training set.txt","w",encoding="utf-8") 
    validation = open("validation set.txt","w",encoding="utf-8") 
    

    
    for i in range(int(num_samples*(1-ratio))):
        game = full.readline()
        #this data cleaning should go in Collect_Data but I don't have the og database to rebuild with the new filter
        if "Z0" not in game and "(" not in game and ")" not in game:
            for board in build_game(game):
                out_text = string_rep(board)
                training.write(out_text)
    for i in range(int(ratio*num_samples)):
        game = full.readline()
        #this data cleaning should go in Collect_Data but I don't have the og database to rebuild with the new filter
        if "Z0" not in game and "(" not in game and ")" not in game:
            for board in build_game(game):
                out_text = string_rep(board)
                validation.write(out_text) 
   
def result_to_num(result):
    result = result.replace("\n", "").replace("'","")
    if result=="1-0":
        return -40
    elif result=="1/2-1/2":
        return 20
    elif result=="0-1":
        return 40
    else:
        print("bad result: ",repr(result))
   
def string_rep(arr):
    out=""
    for n in arr[:-1]:
        out+=str(n)+","
    out+=str(arr[-1])+"\n"
    return out

# get the state of the last move from an incomplete game's sequence
def single_state(game_line):
    split = game_line.split(" ")
    state = s.State()
    state.setup_vanilla()
    
    moves = [string for string in split if "." not in string]
   
   
    for move_text in moves:
        
        state = gen_board(move_text, state)
        if not state:
            # the state was unable to be reached so stop trying to process this game_line
            print("failed to translate: ", move_text)
            return None
    #return a list so that its ready to go for prediction models
    return [state.convert_to_num_array()]
    
if __name__=="__main__":
    start = time.perf_counter()
    build_sets(10000,0.1)
    print("sets generated in ",time.perf_counter()-start)
