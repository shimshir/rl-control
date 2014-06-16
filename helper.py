'''
Created on Jan 13, 2014

@author: admir
'''
from random import random
from math import copysign
import numpy
import math

def randomWCh(numbers, chances):
    rndNum = random()
    cumulative = 0
    for index in range(len(chances)):
        if(rndNum < chances[index] + cumulative):
            return numbers[index]
        cumulative += chances[index]
        
def sampleWCh(samplesWCh):
    rndNum = random()
    cumulative = 0
    for sampleWCh in samplesWCh:
        if(rndNum < sampleWCh[1] + cumulative):
            return sampleWCh[0]
        cumulative += sampleWCh[1]
        
def updateQValue(Qlist, state, action, value):
    for index in range(len(Qlist)):
        if(Qlist[index][0] == state and Qlist[index][1] == action):
            Qlist[index][2] = value
            Qlist[index][3] += 1

def discreteError(error):
    if(abs(error) <= 0.1):
        return 0
    elif(abs(error) > 0.1 and abs(error) <= 1):
        return int(copysign(1, error))
    elif(abs(error) > 1):
        return int(copysign(2, error))
    
def discreteDError(d_error):
    if(abs(d_error) <= 0.003):
        return 0
    elif 0.003 < abs(d_error) <= 0.03:
        return int(copysign(1, d_error))
    elif abs(d_error) > 0.03:
        return int(copysign(2, d_error))
        
    
            
class State():
    def __init__(self, stateVector):
        self.stateVector = stateVector
        
    def __str__(self):       
        return str(self.stateVector)
    
    def __repr__(self):
        return self.__str__()
        
class Reward:
    def __init__(self, state, action, value):
        self.state = state
        self.action = action
        self.value = value
    
    def __str__(self):
        return str([self.state, self.action, round((self.value * 100))/float(100)])
    
    def __repr__(self):
        return self.__str__()

class Q:
    def __init__(self, state, action, value, visits):
        self.state = state
        self.action = action
        self.value = value
        self.visits = visits
    
    def __str__(self):
        return str([self.state, self.action, round((self.value * 100))/float(100), self.visits])
    
    def __repr__(self):
        return self.__str__()
    
class Transition:
    def __init__(self, currentState, action, nextState, chance):
        self.currentState = currentState
        self.action = action
        self.nextState = nextState
        self.chance = chance
    
    def __str__(self):
        return str([self.currentState, self.action, self.nextState, self.chance])
    
    def __repr__(self):
        return self.__str__()
    
def getSign(number):
    if(number >= 0):
        return 1
    else:
        return -1


def deep_copy_matrix(A):
    (m, n) = numpy.shape(A)
    B = numpy.matrix(numpy.zeros(shape=(m, n)))
    for i in range(m):
        for j in range(n):
            B[i, j] = A[i, j]
    return B


def sigmoid(x):
    if x < -1e2:
        return 0
    elif x > 1e2:
        return 1
    return 1 / (1 + math.exp(-x))

vSigmoid = numpy.vectorize(sigmoid)


def boltzmann(net, input_vector, T):
    num = math.exp(net.activate(input_vector) / T)

    denum = math.exp(net.activate([input_vector[0], input_vector[1], input_vector[2],  5]) / T) + math.exp(net.activate([input_vector[0], input_vector[1], input_vector[2], -5]) / T)

    return num / denum


def get_q_indexes(policy, e, de, e_bins):
    if policy > 0:
        policy_index = 1
    else:
        policy_index = 0

    if e <= e_bins[0]:
        e_index = 0
    elif e >= e_bins[-1]:
        e_index = len(e_bins) - 1
    else:
        e_index = numpy.digitize([e], e_bins)[0] - 1

    if de <= -1:
        de_index = 0
    elif abs(de) < 1:
        de_index = 1
    elif de >= 1:
        de_index = 2

    return [policy_index, e_index, de_index]