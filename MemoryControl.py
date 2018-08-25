import random

class MemoryControl:
    def __init__(self, subject, actions):
        self.subject = subject
        self.actions = actions
        self.sequence=[]
        self.changeRatio= abs(random.gauss(.25,.25))
        self.plan=[]
        self.failures={}

    def step(self):
        if self.plan and random.random() > self.changeRatio:
            action=self.plan[0]
            self.plan.pop(0)
        else:
            action = random.choice(self.actions)

        status0='/'.join([str(s) for s in self.subject.getStatus()])
        if status0 in self.failures:
            while action in self.failures[status0]:
                action = random.choice(self.actions)

        try:
            action(self.subject)
            self.sequence.append(action)
        except AttributeError:
            if status0 not in self.failures:
                self.failures[status0]=[]
            self.failures[status0].append(action)

    def run(self,times=100):
        self.subject.reset()
        if self.sequence:
            self.plan=self.sequence[:]
            self.sequence=[]

        for i in range(0,times):
            self.step()

    def shake(self):
        pass




if __name__ == '__main__':
    from WalkingRobot import WalkingRobot
    actionsNames = [methodName for methodName in WalkingRobot.__dict__ if methodName.startswith('move')]
    actions = [getattr(WalkingRobot, actionName) for actionName in actionsNames]
    robot = WalkingRobot()
    print robot.bodyPos, robot.getStatus()


    c=MemoryControl(robot, actions)
    for r in range(1000):
        robot.reset()
        for i in range(1000):
            c.step()

        print robot.bodyPos, robot.getStatus(), len(c.sequence), len(c.failures)
        c.sequence=[]

