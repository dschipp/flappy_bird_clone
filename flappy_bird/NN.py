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
from NN_functions import sigmoid, random_negative_positive

class Neural_Net:
    def __init__(self, input_count, output_count, hidden_layer_count = 5, learning_rate: int = 0.001):
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
        self.hidden_layer_count = hidden_layer_count

        self.weights_input_hidden = np.random.rand(input_count, self.hidden_layer_count)

        self.weights_hidden_output = np.random.rand(self.hidden_layer_count, output_count)

        self.bias_hidden = np.random.rand(1, self.hidden_layer_count)
        self.bias_output = np.random.rand(1, self.output_count)

        self.activation_function = sigmoid

    def calc_outputs(self, inputs: list) -> list:
        """
        Calculate the layers of the Neural Network and give an output.

        Args:
            self (undefined):
            inputs (list): The list of inputs.

        Returns:
            list

        """

        hidden = np.matmul(inputs, self.weights_input_hidden)
        hidden = hidden + self.bias_hidden
        hidden = self.activation_function(hidden)

        output = np.matmul(hidden, self.weights_hidden_output)
        output = output + self.bias_output
        output = self.activation_function(output)

        return output.tolist()[0]



    def adapting(self, NN_to_adapt):
        """
        Adapt the hidden layers from another bird, but slightly different.

        Args:
            self (undefined):
            NN_to_adapt (Neural_Net): The Neural Net to adapt to.

        TODO: Maybe compare the inputted NN decisions with the one this NN made to compare them and the learn from them.

        """

        adapt_rate_weights_input_hidden = random_negative_positive(np.random.rand(self.input_count, self.hidden_layer_count))
        self.weights_input_hidden = NN_to_adapt.weights_input_hidden + adapt_rate_weights_input_hidden * self.learning_rate

        adapt_rate_weights_hidden_output = random_negative_positive(np.random.rand(self.hidden_layer_count, self.output_count))
        self.weights_hidden_output = NN_to_adapt.weights_hidden_output + adapt_rate_weights_hidden_output * self.learning_rate

        adapt_rate_bias_hidden = random_negative_positive(np.random.rand(1, self.hidden_layer_count))
        self.bias_hidden = NN_to_adapt.bias_hidden + adapt_rate_bias_hidden * self.learning_rate

        adapt_rate_bias_output = random_negative_positive(np.random.rand(1, self.output_count))
        self.bias_output = NN_to_adapt.bias_output + adapt_rate_bias_output * self.learning_rate