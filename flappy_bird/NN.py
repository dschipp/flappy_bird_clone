import numpy as np

class Neural_Net:
    def __init__(self, input_count, output_count):
        
        self.hidden_layer = np.random.rand(input_count, output_count)

    def output(self, input):

        result = input * self.hidden_layer

        print(result)