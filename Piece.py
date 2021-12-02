import Move as m
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

class Piece(object):
    
    def __init__(self, type, x, y, value, color):
        self.type =type
        self.x= x
        self.y=y
        self.value = value
        #player =1 for white, player = 0 for black
        self.color =color
        
    def __str__(self):
        return self.type+ m.convert(self.x)+str((8-self.y)) +"\n"
