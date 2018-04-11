import random
from NeuralThing import NeuralNetwork

class NeuralControl:
    def __init__(self, subject, actions, inner_layers=[15]):
        self.subject = subject
        self.actions = actions
        self.sequence = []

        layersSize = [len(self.subject.getStatus())] + inner_layers + [len(actions)]
        self.network = NeuralNetwork(layersSize)

    def shake(self):
        self.network.shake()

    def correct(self,index,change):
        changes = [change if index==i else 0 for i in range(len(self.actions))]
        self.network.correct(changes)

    def step(self):
        def selectMaxValue(values):
            return values.index(max(values))
        def selectAValueAboveThreshold(values,th=1):
            positiveIndex = [i for i, v in enumerate(outValues) if v > th]
            if len(positiveIndex)>0:
                return random.choice(positiveIndex)
            else:
                return selectMaxValue(values)

        status = self.subject.getStatus()
        outValues = self.network.evaluate(status)
        nextActionIndex = selectAValueAboveThreshold(outValues)
        nextAction = self.actions[nextActionIndex]
        try:
            nextAction(self.subject)
            self.sequence.append(nextAction)
            self.correct(nextActionIndex,.01)
        except AttributeError:
            sortedValues = sorted(outValues)
            #self.correct(nextActionIndex, sortedValues[-2]-sortedValues[-1]-.1)
            self.correct(nextActionIndex, -.01)

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
                if hasattr(neuron,'weights'):
                    stepWeights += neuron.weights
        self.weights.append(stepWeights)


