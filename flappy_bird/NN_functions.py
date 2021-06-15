from numpy import exp
from random import randint

def decision_function(input):
    if input[1] >= input[0]:
        return True
    return False

def sigmoid(x):
    x = 1 / (1 + exp(-x))
    return x

def random_negative_positive(x):
    return x * randint(-1, 1)