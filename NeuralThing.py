import random
from contextPrint import ContextPrint
cp=ContextPrint()


def sign(value):
    return 1 if value >= 0 else -1


def randrange(start,stop):
    return start+(stop-start)*random.random()


class FixNeuron():
    def __init__(self, value=1):
        self.value = value
        self.weights=[]
    def learn(self, delta):
        pass
    def evaluate(self):
        pass
    def shake(self):
        pass

class Neuron:
    def __init__(self,inputs = None):
        self.entries=[]  #list of neruons
        self.weights=[]
        self.value = 0
        if inputs is not None:
            for input in inputs:
                self.append(input)

    def evaluate(self):
        if self.entries:
            self.value = sum([entry.value*weight for entry, weight in zip(self.entries, self.weights)])

    def shake(self):
        for i in range(len(self.weights)):
            self.weights[i] += randrange(-.1,.1)

    def randomWeight(self):
        return randrange(-1, 1)

    def append(self,neuron,weight = None):
        if not self.entries:
            self.entries.append(FixNeuron())
            self.weights.append(self.randomWeight())

        self.entries.append(neuron)
        self.weights.append(weight if weight is not None
                                   else self.randomWeight())
    def learn(self, delta):
        if not self.entries or not delta:
            return
        cp.push("Neuron.learn")
        #cp.cprint("delta:",delta, "value:", self.value)
        #cp.cprint("w0",self.weights)
        weightedvalues = [abs(weight*entry.value) for weight, entry in zip(self.weights,self.entries)]
        sumwvalues= sum(weightedvalues)
        deltas = [delta* weightedvalue/sumwvalues for weightedvalue in weightedvalues]
        #deltas = [delta* weight*entry.value/self.value for weight, entry in zip(self.weights,self.entries)]

        for i in range(len(self.entries)):
            if self.entries[i].value:
                self.weights[i] += deltas[i]/2./self.entries[i].value#/(self.entries[i].value-deltas[i])
        #cp.cprint("w1",self.weights)

        for edelta, entry, weight in zip(deltas, self.entries, self.weights):
            #cp.cprint("prop", entry.value, weight, edelta)
            entry.learn(edelta/2./weight)
        cp.pop()


class NeuralNetwork:
    def __init__(self, layersSize):

        self.neuronLayer=[]
        for l in layersSize:
            if not self.neuronLayer :
                self.neuronLayer.append([FixNeuron() for _ in range(l)])
            else:
                self.neuronLayer.append([Neuron(self.neuronLayer[-1]) for _ in range(l)])
            if l is not layersSize[-1]:
                self.neuronLayer[-1].append(FixNeuron())

    def shake(self):
        for layer in self.neuronLayer[1:]:
            for neuron in layer:
                neuron.shake()

    def evaluate(self, inValues):
        cp.push("Evaluate")
        vis=inValues
        for inValue,neuron in zip(inValues, self.neuronLayer[0]):
            neuron.value = inValue
        for layer in self.neuronLayer:
            for neuron in layer:
                neuron.evaluate()
            #cp.cprint([neuron.value for neuron in layer])
        cp.pop()
        return [neuron.value for neuron in self.neuronLayer[-1]]

    def correct(self, changes):
        for neuron, change in zip(self.neuronLayer[-1], changes):
            neuron.learn(change)


import unittest


#@unittest.skip("")
class NeuronTest(unittest.TestCase):
    def setInputs(self,inputs,values):
        for input,v in zip(inputs,values):
            input.value = v

    def test_create(self):
        inputs = [Neuron() for i in range(3)]
        neuron = Neuron(inputs)

    def test_evaluate0(self):
        inputs = [Neuron() for i in range(3)]
        neuron = Neuron(inputs)
        self.setInputs(inputs,[0,.5,0])
        neuron.evaluate()
        self.assertEqual(neuron.value, .5*neuron.weights[1])

    def test_evaluate1(self):
        inputs = [Neuron() for i in range(3)]
        neuron = Neuron(inputs)
        self.setInputs(inputs,[1.,1.,1.])
        neuron.evaluate()
        self.assertEqual(neuron.value, sum(neuron.weights))

    def test_learn(self):
        inputs = [Neuron() for i in range(3)]
        neuron = Neuron(inputs)
        self.setInputs(inputs,[1.,0.,0.])
        neuron.evaluate()
        v0=neuron.value
        neuron.learn(-.1)
        neuron.evaluate()
        v1=neuron.value
        self.assertLess(v1, v0)

    def test_learn2(self):
        inputs = [Neuron() for i in range(3)]
        neuron = Neuron(inputs)
        self.setInputs(inputs,[1.,1.,1.])
        neuron.evaluate()
        v0=neuron.value
        neuron.learn(.1)
        neuron.evaluate()
        v1=neuron.value
        self.assertGreater(v1, v0)


class NeuralNetworkTest(unittest.TestCase):
    #@unittest.skip("")
    def test_create(self):
        nn=NeuralNetwork([3,4,2])
        self.assertEqual(len(nn.neuronLayer),3)
        self.assertEqual(len(nn.neuronLayer[0]), 3)
        self.assertEqual(len(nn.neuronLayer[1]), 4)
        self.assertEqual(len(nn.neuronLayer[2]), 2)

    #@unittest.skip("")
    def test_correct_onelayer(self):
        nn=NeuralNetwork([2,3])
        v0=nn.evaluate([0,1])
        nn.correct([0, .1, -.1])
        v1=nn.evaluate([0,1])
        self.assertEqual(v1[0],v0[0])
        self.assertGreater(v1[1],v0[1])
        self.assertLess(v1[2],v0[2])

    def test_correct_twolayers(self):
        cp.push("test_correct_twolayers")
        nn=NeuralNetwork([2,3,3])
        v0=nn.evaluate([0,1])
        nn.correct([0, .1, -.1])
        v1=nn.evaluate([0,1])
        self.assertGreater(v1[1],v0[1])
        self.assertLess(v1[2],v0[2])
        cp.pop()

if __name__ == '__main__':
    unittest.main()
