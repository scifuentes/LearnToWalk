from copy import deepcopy

class Pos:
    def __init__(self,x=0,y=0,z=0):
        self.x=x
        self.y=y
        self.z=z
    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        self.z += other.z
        return self
    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        self.z -= other.z
        return self
    def __nonzero__(self):
        return (self.x!=0 and self.y!=0 and self.z!=0)

    def __str__(self):
        return str([self.x, self.y, self.z])


class WalkingRobot:
    def __init__(self):
        self.reset()
        self.xLim = 5
        self.yLim = 2
        self.zLim = 1

    def reset(self):
        self.bodyPos=Pos()
        self.legs = [Pos(), Pos(), Pos(), Pos()]


    def _moveLegs(self,frMove=Pos(),flMove=Pos(),brMove=Pos(),blMove=Pos()):
        moves = [frMove, flMove, brMove, blMove]
        for leg, move in zip(self.legs, moves):
            if(leg.z==0 and (move.x!=0 or move.y!=0)):
                raise AttributeError
        legsCopy = deepcopy(self.legs)
        for leg, move in zip(legsCopy, moves):
            leg += move
        self._checkLegs(legsCopy)
        self.legs = deepcopy(legsCopy)

    def _moveBody(self,move=Pos()):
        legsCopy = deepcopy(self.legs)
        for leg in legsCopy:
            if leg.z == 0:
                leg -= move
        self._checkLegs(legsCopy)
        self.legs = deepcopy(legsCopy)
        self.bodyPos += move

    def _checkLegs(self, legs):
        groundLegs=0
        for leg in legs:
            if ( leg.z > self.zLim or leg.z < 0 or
                 abs(leg.x) > self.xLim or
                 abs(leg.y) > self.yLim ):
                    raise AttributeError
            if leg.z == 0:
                groundLegs += 1
        if groundLegs <3:
            raise AttributeError

    def __str__(self):
        return ", ".join(map(str,[self.bodyPos, [str(leg) for leg in self.legs]]))

    def getStatus(self):
        return [leg.x for leg in self.legs] + [leg.z for leg in self.legs]

    def moveBodyFront(self, m=Pos(1,0,0)):
        self._moveBody(m)
    #def moveBodyBack(self, m=Pos(-1,0,0)):
    #    self._moveBody(m)

    def moveLegFRUp(self, m=Pos(0,0,1)):
        self._moveLegs(frMove=m)
    def moveLegFRDown(self, m=Pos(0,0,-1)):
        self._moveLegs(frMove=m)
    def moveLegFRFront(self, m=Pos(1,0,0)):
        self._moveLegs(frMove=m)
    #def moveLegFRBack(self, m=Pos(-1,0,0)):
    #    self._moveLegs(frMove=m)
    def moveLegFLUp(self, m=Pos(0,0,1)):
        self._moveLegs(flMove=m)
    def moveLegFLDown(self, m=Pos(0,0,-1)):
        self._moveLegs(flMove=m)
    def moveLegFLFront(self, m=Pos(1,0,0)):
        self._moveLegs(flMove=m)
    #def moveLegFLBack(self, m=Pos(-1,0,0)):
    #    self._moveLegs(flMove=m)
    def moveLegBRUp(self, m=Pos(0,0,1)):
        self._moveLegs(brMove=m)
    def moveLegBRDown(self, m=Pos(0,0,-1)):
        self._moveLegs(brMove=m)
    def moveLegBRFront(self, m=Pos(1,0,0)):
        self._moveLegs(brMove=m)
    #def moveLegBRBack(self, m=Pos(-1,0,0)):
    #    self._moveLegs(brMove=m)
    def moveLegBLUp(self, m=Pos(0,0,1)):
        self._moveLegs(blMove=m)
    def moveLegBLDown(self, m=Pos(0,0,-1)):
        self._moveLegs(blMove=m)
    def moveLegBLFront(self, m=Pos(1,0,0)):
        self._moveLegs(blMove=m)
    #def moveLegBLBack(self, m=Pos(-1,0,0)):
    #    self._moveLegs(blMove=m)

