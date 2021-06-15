"""
This is going to be a Neural Network with 2 hiddep layers consisting of a specified number of neurons.

So there is going to be needed a Matrix with the size of the number of inputs and hidden layer one.

For example if we have 3 inputs and a number of 5 hidden layer neurons: 

                 | r  r  r |     | output_1 |
| input_1 |      | r  r  r |     | output_2 |
| input_2 |  *   | r  r  r |  =  | output_3 |
| input_3 |      | r  r  r |     | output_4 |
                 | r  r  r |     | output_5 |

the outputs go in the next hidden layer and then an out put is created.

So we need 3 matrices that have the size of:

1. number of inputs x fist hidden layer neurons
2. fist hidden layer neurons x second hidden layer neurons
3. second hidden layer neurons x number of outputs

These matrices are getting multiplied and in a separate function you can change the values of the hidden layer 
matrices slidely to train.

To learn the NN gets another NN as input and then adapts the hidden layers of that NN slightly different.

"""

import numpy as np
import random

HIDDEN_NEURON_COUNT_1 = 5
HIDDEN_NEURON_COUNT_2 = 5


class Neural_Net:
    def __init__(self, input_count, output_count, learning_rate: int = 0.01):
        """
        Create Neural Network width 2 Hidden layers.

        Args:
            self (undefined):
            input_count (undefined): The number of inputs.
            output_count (undefined): The number of outputs.
            learning_rate (int = 1): The learning rate of the NN, when adapting.

        """

        self.learning_rate = learning_rate
        self.output_count = output_count
        self.input_count = input_count

        """
        self.hidden_layer_1 = np.random.rand(
            input_count, HIDDEN_NEURON_COUNT_1)
        self.hidden_layer_2 = np.random.rand(
            HIDDEN_NEURON_COUNT_2, HIDDEN_NEURON_COUNT_1)
        self.output_layer = np.random.rand(output_count, HIDDEN_NEURON_COUNT_2).reshape(
            HIDDEN_NEURON_COUNT_2, output_count)
        """

        self.output_layer = np.random.rand(output_count, input_count).reshape(
            input_count, output_count)

    def calc_outputs(self, inputs: list) -> list:
        """
        Calculate the layers of the Neural Network and give an output.

        Args:
            self (undefined):
            inputs (list): The list of inputs.

        Returns:
            list

        """

        inputs = np.array(inputs).reshape(1, len(inputs))
    
        """ normalisation = sum(inputs)

        output = np.matmul(inputs, self.hidden_layer_1) / normalisation
        normalisation = sum(output.reshape(HIDDEN_NEURON_COUNT_1, 1))

        output = np.matmul(output, self.hidden_layer_2) / normalisation
        
        normalisation = sum(output.reshape(HIDDEN_NEURON_COUNT_2, 1))
        output = np.matmul(output, self.output_layer) / normalisation """

        normalisation = sum(inputs.reshape(self.input_count, 1))
        output = np.matmul(inputs, self.output_layer) / normalisation

        return output.tolist()[0]

    def adapting(self, NN_to_adapt):
        """
        Adapt the hidden layers from another bird, but slightly different.

        Args:
            self (undefined):
            NN_to_adapt (Neural_Net): The Neural Net to adapt to.

        """

        """ adapt_rate = np.random.rand(self.input_count, HIDDEN_NEURON_COUNT_1) * random.randint(-1,1)
        self.hidden_layer_1 = NN_to_adapt.hidden_layer_1 + adapt_rate * self.learning_rate

        adapt_rate = np.random.rand(HIDDEN_NEURON_COUNT_2, HIDDEN_NEURON_COUNT_1) * random.randint(-1,1)
        self.hidden_layer_2 = NN_to_adapt.hidden_layer_2 + adapt_rate * self.learning_rate

        adapt_rate = np.random.rand(self.output_count, HIDDEN_NEURON_COUNT_2).reshape(HIDDEN_NEURON_COUNT_2, self.output_count) * random.randint(-1,1)
        self.output_layer = NN_to_adapt.output_layer + adapt_rate * self.learning_rate """

        adapt_rate = np.random.rand(self.output_count, self.input_count).reshape(self.input_count, self.output_count) * random.randint(-1,1)
        self.output_layer = NN_to_adapt.output_layer + adapt_rate * self.learning_rate