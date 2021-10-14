import Move as M
class State:
    
    def __init__(self):
        self.blackPieces=[]
        self.whitePieces=[]
        self.board=[]
        
    def generateSuccessor(self,move):
        new = self.deepcopy()
        new.play_move(move)
        return new
    
    def play_move(self, move):
        