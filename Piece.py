import Move as M
class Piece:
    
    def __init__(self, type, color, x, y):
        self.type =type
        self.color=color
        self.x= x
        self.y=y
        
    def __str__(self):
        return self.color +" "+ self.type + " " + M.convert(self.x)+str((8-self.y)) +"\n"
