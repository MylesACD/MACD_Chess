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

class Move(object):
    
    def __init__(self,piece,sx,sy,cap,ex,ey,extra):
        self.piece = piece
        self.sx = sx
        self.sy=sy
        self.cap = cap
        self.ex =ex
        self.ey =ey
        self.extra =extra
        
    def __str__(self):
        return str(self.piece) + convert_to_letter(self.sx) +str(8-self.sy)+self.cap + convert_to_letter(self.ex) + str(8-self.ey) +self.extra +"\n"
        
def convert_to_letter(num):
    if num==0:
        return "a"
    elif num==1:
        return "b"
    elif num==2:
        return "c"
    elif num==3:
        return "d"
    elif num==4:
        return "e"
    elif num==5:
        return "f"
    elif num==6:
        return "g"
    elif num==7:
        return "h"