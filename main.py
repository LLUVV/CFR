import random
import matplotlib.pyplot as plt
import math
import numpy

# Practice Counterfactual Regret Minimization - Colonel Blotto

S = 5
N = 3
numChoice = int(math.factorial(S+N-1) / math.factorial(S) / math.factorial(N-1))
myRegretSum = [0.0] * numChoice
myStrategy = [0.0] * numChoice
myStrategySum = [0.0] * numChoice
oppRegretSum = [0.0] * numChoice
oppStrategy = [0.0] * numChoice
oppStrategySum = [0.0] * numChoice
myActualDtb = [0] * N
oppActualDtb = [0] * N
myResult = []
oppResult = []

def GetAction(strategy):
    ran = random.random()
    sum = 0.0
    for i in range(len(strategy)):
        sum += strategy[i]
        if(ran <= sum):
            return i

def GetActualDtb(action):
    dtb = [0] * N
    sum = -1
    for i in range(6):
        sum += 6-i
        if action <= sum:
            dtb[0] = i
            sum -= action
            break
    dtb[1] = 5 - dtb[0] - sum
    dtb[2] = sum
    return dtb

def GetUtility(dtb1,dtb2):
    utility1 = 0
    utility2 = 0
    for i in range(N):
        if(dtb1[i] > dtb2[i]):
            utility1 += 1
        elif(dtb1[i] < dtb2[i]):
            utility2 += 1
    if(utility1 > utility2):
        return utility1
    else:
        return 0

def GetRegret(myDtb,oppDtb):
    utility = GetUtility(myDtb,oppDtb)
    regret = [0.0] * numChoice
    for i in range (numChoice):
        nowDtb = GetActualDtb(i)
        nowUtility = GetUtility(nowDtb,oppDtb) - utility
        regret[i] = nowUtility if nowUtility > 0 else 0
    return regret

def GetStrategy(regret):
    strategy = [0.0] * numChoice
    normalizeSum = 0.0
    for i in regret:
        normalizeSum += i
    for i in range(numChoice):
        if normalizeSum == 0 :
            strategy[i] = 1/numChoice
        else:
            strategy[i] = regret[i] / normalizeSum if regret[i] > 0 else 0
    return strategy

def Train(iteration):
    for i in range(iteration):
        global myStrategy, oppStrategy, myRegretSum, oppRegretSum, myActualDtb, oppActualDtb
        myStrategy = GetStrategy(myRegretSum)
        oppStrategy = GetStrategy(oppRegretSum)
        myActualDtb = GetActualDtb(GetAction(myStrategy))
        oppActualDtb =  GetActualDtb(GetAction(oppStrategy))
        myRegret = GetRegret(myActualDtb,oppActualDtb)
        oppRegret = GetRegret(oppActualDtb,myActualDtb)
        for j in range(numChoice):
            myRegretSum[j] += myRegret[j]
            oppRegretSum[j] += oppRegret[j]
        GetAverageStrategy()

def GetAverageStrategy():
    global myRegretSum,oppRegretSum,myResult,oppResult
    myAvgStrategy = [0.0] * numChoice
    oppAvgStrategy = [0.0] * numChoice
    normalizeSum1 = 0.0
    normalizeSum2 = 0.0
    for i in range(numChoice):
        normalizeSum1 += myRegretSum[i]
        normalizeSum2 += oppRegretSum[i]
    for i in range(numChoice):
        if normalizeSum1 == 0 :
            myAvgStrategy[i] = 1/numChoice
        else:
            myAvgStrategy[i] = myRegretSum[i] / normalizeSum1 if myRegretSum[i] > 0 else 0
        if normalizeSum2 == 0 :
            oppAvgStrategy[i] = 1/numChoice
        else:
            oppAvgStrategy[i] = oppRegretSum[i] / normalizeSum2 if oppRegretSum[i] > 0 else 0
    print(myAvgStrategy)
    print(oppAvgStrategy)
    myResult.append(myAvgStrategy)
    oppResult.append(oppAvgStrategy)

if __name__ == "__main__":
    Train(2000)
    plt.plot(myResult,'-')
    plt.plot(oppResult,'--')
    plt.ylabel('Probability')
    plt.xlabel('iteration')
    plt.show()
