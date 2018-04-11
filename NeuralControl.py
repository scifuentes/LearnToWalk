import random
from NeuralThing import NeuralNetwork

class NeuralControl:
    def __init__(self, subject, actions, inner_layers=[15]):
        self.subject = subject
        self.actions = actions
        self.sequence = []

        self.layerSize = [len(self.subject.getStatus()) + 1] + inner_layers + [len(actions)]
        self.network = NeuralNetwork(self.layerSize)

    def shake(self):
        self.network.shake()

    def correct(self,index,change):
        changes = [change if index==i else 0 for i in range(len(self.actions))]
        self.network.correct(changes)

    def step(self):
        def selectMaxValue(values):
            return values.index(max(values))
        def selectAValueAbove0(values):
            positiveIndex = [i for i, v in enumerate(outValues) if v > 0]
            if len(positiveIndex)>0:
                return random.choice(positiveIndex)
            else:
                return selectMaxValue(values)

        status = self.subject.getStatus()
        outValues = self.network.evaluate(status)
        nextActionIndex = selectAValueAbove0(outValues)
        nextAction = self.actions[nextActionIndex]
        try:
            nextAction(self.subject)
            self.sequence.append(nextAction)
            self.correct(nextActionIndex,.1)
        except AttributeError:
            sortedValues = sorted(outValues)
            #self.correct(nextActionIndex, sortedValues[-2]-sortedValues[-1]-.1)
            self.correct(nextActionIndex, -.1)

    def run(self,times=100):
        self.subject.reset()
        for i in range(0,times):
            self.step()



class NeuralTracker(NeuralControl):
    def __init__(self, subject, actions, inner_layers=[15]):
        NeuralControl.__init__(self, subject, actions, inner_layers)
        self.weights=[]

    def run(self, steps):
        self.subject.reset()
        for i in range(0,steps):
            self.step()
            self.storeWeights()

    def storeWeights(self):
        stepWeights=[]
        for layer in self.network.neuronLayer:
            for neuron in layer:
                stepWeights += neuron.weights
        self.weights.append(stepWeights)


if __name__  == '__main__':
    from XorFunction import XorFunction
    import matplotlib.pyplot as plt
    plt.plot([1, 2, 3, 4])

    actionsNames = ['r0','r1']
    actions = [XorFunction.result0, XorFunction.result1]
    actionsDic = {action: name for action, name in zip(actions, actionsNames)}

    t=NeuralTracker(XorFunction(),actions,[])
    t.run(10000)
    #print len(t.sequence), t.subject.bodyPos.x, t.subject
    print len(t.sequence), t.subject
    print [actionsDic[action] for action in t.sequence]
    #for weights0,weights1 in zip(t.weights[:-1],t.weights[1:]):
    #    print max([abs(weight0-weight1) for weight0, weight1 in zip(weights0,weights1)])

    plt.plot(t.weights)
    plt.show()
