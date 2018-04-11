import random

class RandomControl:
    def __init__(self, subject, actions):
        self.subject = subject
        self.actions = actions
        self.sequence=[]
        self.changeRatio= abs(random.gauss(.25,.25))
        self.plan=[]

    def step(self):
        if self.plan and random.random() > self.changeRatio:
            action=self.plan[0]
            self.plan.pop(0)
        else:
            action = random.choice(self.actions)
        try:
            action(self.subject)
            self.sequence.append(action)
        except AttributeError:
            pass

    def run(self,times=100):
        self.subject.reset()
        if self.sequence:
            self.plan=self.sequence[:]
            self.sequence=[]

        for i in range(0,times):
            self.step()






if __name__ == '__main__':
    rw = RandomControl()
    rw.run()

    print len(rw.sequence)
    print rw.sequence
    print rw.walker

