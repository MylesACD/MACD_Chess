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
        self.has_not_moved = True
        
    def __str__(self):
        return self.type+ m.convert(self.x)+str((8-self.y)) +"\n"
    
    def deep_clone(self):
        clone = Piece(self.type,self.x,self.y,self.value,self.color)
        clone.has_not_moved = self.has_not_moved
        return clone
        
    
    def translate_to_pgn(self):
        if self.type == wk or self.type == bk:
            return "K"
        elif self.type == wp or self.type == bp:
            return ""
        elif self.type == wb or self.type == bb:
            return "B"
        elif self.type == wn or self.type == bn:
            return "N"
        elif self.type == wr or self.type == br:
            return "R"
        elif self.type == wq or self.type == bq:
            return "Q"