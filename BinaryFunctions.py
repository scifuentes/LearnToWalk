import random

class BinaryFunction:
    def __init__(self):
        self.entries=[]
    def reset(self):
        pass
    def getStatus(self):
        self.entries=[random.choice([-1,1]),random.choice([-1,1])]
        return self.entries
    def rFalse(self):
        if self.isTrue():
            raise AttributeError
    def rTrue(self):
        if not self.isTrue():
            raise AttributeError

class XorFunction(BinaryFunction):
    def isTrue(self):
        return self.entries[0] != self.entries[1]

class OrFunction(BinaryFunction):
    def isTrue(self):
        return (self.entries[0]==1 or self.entries[1]==1)

class AndFunction(BinaryFunction):
    def isTrue(self):
        return (self.entries[0]==1 and self.entries[1]==1)
