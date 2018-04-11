from XorFunction import XorFunction
from NeuralControl import NeuralTracker
import matplotlib.pyplot as plt

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
