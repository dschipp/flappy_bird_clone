from numpy import exp
from random import randint


def decision_function(input):
    """
    The function after what the bird decides what to do.

    Args:
        input (undefined): The Input List

    """
    if input[1] >= input[0]:
        return True
    return False


def sigmoid(x: int):
    """
    The sigmoid function

    Args:
        x (int): The x input

    """
    x = 1 / (1 + exp(-x))
    return x


def random_negative_positive(x: int):
    """
    Return the input random negative of positive.

    Args:
        x (int): The input

    """
    return x * randint(-1, 1)
