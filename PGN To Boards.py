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

pgn = "1. e4 e5 2. Nf3 Qf6 3. Bc4 Qg6 4. O-O Qxe4 5. Bxf7+ Kxf7 6. Ng5+ Ke8 7. Nxe4 1-0"

"""
def convert(s):
    if s=="a":
        return 0
    elif s=="b":
        return 1
    elif s=="c":
        return 2
    elif s=="d":
        return 3
    elif s=="e":
        return 4
    elif s=="f":
        return 5
    elif s=="g":
        return 6
    elif s=="h":
        return 7    
"""

def gen_board(move_text,state):
    move_text = move_text.replace("+","")
    move_text = move_text.replace("#","")
    
    possible_moves = state.generate_all_moves()
    print(len(possible_moves))
    
    for move in possible_moves:
        # other than checks if the move strings are the same
        if str(move).replace("+", "").replace("#", "") == move_text:
            return state.generateSuccesor(move)
    
    print("failed for:" , move_text)

def build_game(game_line):
    split = game_line.split(" ")
    state = s.State()
    state.setup_vanilla()
    result = split[-1]
    moves = [string for string in split if "." not in string]
    moves = moves[:-1]
    # for testing only
    moves = moves[:2]
    boards=[str(state)]
    
    for move_text in moves:
        state = gen_board(move_text, state)
        if state:
            boards.append(state)

    return boards

bs = build_game(pgn)

for grid in bs:
    print(grid)
