import random
import matplotlib.pyplot as plt
import numpy as np
from itertools import product

SOLDIERS = 5
FIELDS = 3
NUM_ACTIONS = 0
valid_actions = []

class Player:
    def __init__(self):
        self.regretSum = [0.0] * NUM_ACTIONS
        self.strategy = [0.0] * NUM_ACTIONS
        self.strategySum = [0.0] * NUM_ACTIONS
        self.result = []

    def getStrategy(self):
        normalizingSum = 0.0
        for a in range(NUM_ACTIONS):
            if self.regretSum[a] > 0:
                self.strategy[a] = self.regretSum[a]
            else:
                self.strategy[a] = 0
            normalizingSum += self.strategy[a]
        for a in range(NUM_ACTIONS):
            if normalizingSum > 0:
                self.strategy[a] /= normalizingSum
            else:
                self.strategy[a] = 1.0 / NUM_ACTIONS
            normalizingSum += self.strategy[a]
        return self.strategy

    def getAction(self):
        r = random.random()
        a = 0
        cumulativeProbability = 0.0
        while a < NUM_ACTIONS - 1:
            cumulativeProbability += self.strategy[a]
            if r < cumulativeProbability:
                break
            a += 1
        return a

    def getActionUtility(self, oppAction):
        Utility = [0.0] * NUM_ACTIONS
        for i in range(NUM_ACTIONS):
            Utility[i] = self.cmp(i, oppAction)
        return Utility

    def cmp(self, myidx, oppidx):
        count = 0
        myAction = valid_actions[myidx]
        oppAction = valid_actions[oppidx]
        for i in range(FIELDS):
            count += myAction[i] > oppAction[i]
            count -= myAction[i] < oppAction[i]
        return count

    def getAverageStrategy(self):
        avgStrategy = [0.0] * NUM_ACTIONS
        normalizingSum = 0.0
        for a in range(NUM_ACTIONS):
            normalizingSum += self.strategySum[a]
        for a in range(NUM_ACTIONS):
            if normalizingSum > 0:
                avgStrategy[a] = self.strategySum[a] / normalizingSum
            else:
                avgStrategy[a] = 1.0 / NUM_ACTIONS
            self.strategySum[a] += self.strategy[a]
        return avgStrategy

def create_actions(soldiers, fields):
    for i in product(range(soldiers+1), repeat=fields):
        if sum(i) == soldiers:
            valid_actions.append(i)

def train(iterations, P1, P2):
    for i in range(iterations):
        # get regret-matched mixed-strategy actions
        P1.getStrategy()
        P2.getStrategy()
        P1Action = P1.getAction()
        P2Action = P2.getAction()

        # compute action utilities
        P1actionUtility = P1.getActionUtility(P2Action)
        P2actionUtility = P2.getActionUtility(P1Action)

        # accumulate action regrets
        for a in range(NUM_ACTIONS):
            P1.regretSum[a] += P1actionUtility[a] - P1actionUtility[P1Action]
            P2.regretSum[a] += P2actionUtility[a] - P2actionUtility[P2Action]

if __name__ == "__main__":
    create_actions(SOLDIERS, FIELDS)
    NUM_ACTIONS = len(valid_actions)
    P1 = Player()
    P2 = Player()

    for t in range(10):
        # perform 10 experiments
        print("----------------------------------")
        P1 = Player()
        P2 = Player()
        for i in range(100000):
            train(1, P1, P2)
            # print("P1 strategy:", getAverageStrategy(P1))
            # print("P2 strategy:", getAverageStrategy(P2))
            P1.result.append(P1.getAverageStrategy())
            P2.result.append(P2.getAverageStrategy())

        # print top 3 actions in the average strategy
        P1Strategy = P1.getAverageStrategy()
        sort_idx = np.argsort(P1Strategy)
        for i in range(3):
            print(valid_actions[sort_idx[i-3]])

        # print dominant actions in the average strategy
        # print("----------------------------------")
        # for i in range(len(P1Strategy)):
        #     if P1Strategy[i] > 0.05:
        #         print(valid_actions[i])
        # print("----------------------------------")

    # print("P1 strategy:", P1Strategy)
    # plt.plot(P1.result)
    # plt.ylabel('P1 Probability')
    # plt.show()

    # plt.plot(P2.result)
    # plt.ylabel('P2 Probability')
    # plt.show()