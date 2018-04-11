from WalkTrainer import Trainner
from RandomControl import RandomControl
from NeuralControl import NeuralControl


def trainControllers(controllers, generations=10):
    controlEvolution=[]
    for control in controllers:
        controlEvolution.append(Trainner(control).train(generations))

    print
    print 'Training Evolution:'
    for evolution,control in zip(controlEvolution,controllers):
        print control.__name__, [result.value for result in evolution]

if __name__ == '__main__':
    trainControllers([RandomControl,NeuralControl],5)


