import random

class XorFunction:
    def __init__(self):
        self.entries=[]
    def reset(self):
        pass
    def getStatus(self):
        self.entries=[random.choice([-1,1]),random.choice([-1,1])]
        return self.entries
    def result0(self):
        if self.entries[0] == self.entries[1]:
            raise AttributeError
        else:
            pass
    def result1(self):
        if self.entries[0] != self.entries[1]:
            raise AttributeError
        else:
            pass

