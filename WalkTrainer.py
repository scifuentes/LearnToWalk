from copy import deepcopy
from WalkingRobot import WalkingRobot
import random
class Struct:
    pass

actionsNames = [methodName for methodName in WalkingRobot.__dict__ if methodName.startswith('move')]
actions = [getattr(WalkingRobot, actionName) for actionName in actionsNames]
actionsDic = {action:name for action, name in zip(actions, actionsNames)}

class Trainner:
    def __init__(self, ControlClass, population=100):
        self.cnt = 0
        self.ControlClass = ControlClass
        print self.ControlClass.__name__
        self.controlers = [self.createNewControler() for _ in range(population)]

    def createNewControler(self):
        control = self.ControlClass(WalkingRobot(), actions)
        control.name = 'N'+str(self.cnt)
        self.cnt += 1
        return control

    def train(self, generations, steps=100 ):
        bestResults = []
        for i in range(generations):
            print "Generation", i
            results = self.runGeneration()
            sorted_results = self.sortedResults(results)
            bestResults.append(sorted_results[0])
            self.controlers = self.select_new_generation(sorted_results)
        return bestResults

    def runGeneration(self, steps=200):
        for control in self.controlers:
            control.sequence = []
            control.subject.reset()

        results = []
        for controler in self.controlers:
            controler.run(steps)
            if True:#control.object.bodyPos.x>5:
                result=Struct()
                result.controler=controler
                # result.travel = controler.subject.bodyPos.x
                #result.travel = (controler.subject.legs[0].x+controler.subject.legs[1].x+controler.subject.legs[2].x+controler.subject.legs[3].x)/4
                result.travel = controler.subject.bodyPos.x #+ min(controler.subject.legs[0].x,controler.subject.legs[1].x,controler.subject.legs[2].x,controler.subject.legs[3].x)
                result.sequence = controler.sequence
                results.append(result)

        return results

    def sortedResults(self, results):
        def distance(result):
            return result.travel
        def distanceAndEfficiency(result):
            efficiency = float(result.travel)/(len(result.sequence)+1)
            result.value = result.travel + efficiency
            return result.value
        def distanceAndIdealSteps(result):
            idealSteps = 4.0 * result.travel
            steps = len(result.sequence)
            minSteps = result.travel
            result.value = result.travel
            if result.travel>0:
                if steps > idealSteps:
                    result.value += idealSteps/steps*.99
                else:
                    result.value += (steps-minSteps)/(idealSteps-minSteps)*.99
            return result.value

        return  sorted(results, key=distanceAndIdealSteps, reverse=True)

    def select_new_generation(self, sorted_results):
        def printBestResults():
            print [result.travel for result in sorted_results]
            for result in sorted_results[0:min(len(sorted_results), 3)]:
                actionList = [actionsDic[action] for action in result.sequence]
                #print result.value, result.travel, len(actionList), result.controler.name, actionList

        printBestResults()

        top_controlers = [result.controler for result in sorted_results[0:10]]
        random_controllers = [result.controler for result in random.sample(sorted_results,min(len(sorted_results),5))
                                               if result.controler not in top_controlers]
        new_controllers = []#[self.createNewControler() for i in range(10)]
        selected_controlers = top_controlers + random_controllers + new_controllers

        new_generation = selected_controlers[:]
        for i in range(len(sorted_results)-len(selected_controlers)):
            child_controller = deepcopy(random.choice(selected_controlers))
            child_controller.name += '.'+str(i)
            child_controller.shake()
            new_generation.append(child_controller)

        return new_generation



if __name__ == '__main__':
    #from NeuralControl import NeuralControl
    #Trainner(NeuralControl).train(10, 200)

    from RandomControl import RandomControl
    Trainner(RandomControl,1).train(100, 100)

    from MemoryControl import MemoryControl
    Trainner(MemoryControl,1).train(100, 100)
