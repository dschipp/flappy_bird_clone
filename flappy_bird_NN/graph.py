import constants
from bird import flappy_bird
import numpy as np
import pyglet
import os
import sys
path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(path)
__docformat__ = "google"

"""
This shall be a file where graphs are beeing plotted.
"""


class NN_graph():
    def __init__(self) -> None:
        """
        Create graph that displays the NN of the Birds. 
        The opacity of the objects are based on the value of the bias or weight. So the opacity of the lines between the neurons are dependent on the weight between the neurons. The opacity of the circles are dependent on the bias value of that neuron.

        TODO: Implement a change of the opacity to the input values.
        TODO: Implement in someway which input is most important an lead to a significant change to the output.

        Args:
            self (undefined):

        Returns:
            None

        """
        self.input_num = constants.NN_INPUT_NUM
        self.output_num = constants.NN_OUTPUT_LAYER_NUM
        self.hidden_num = constants.NN_HIDDEN_LAYER_NUM

        weights_input_hidden = np.random.rand(
            self.input_num, self.hidden_num)

        weights_hidden_output = np.random.rand(
            self.hidden_num, self.output_num)

        dist_between_layers = constants.NN_GRAPH_DIST_BETWEEN_LAYERS
        dist_between_neurons = constants.NN_GRAPH_DIST_BETWEEN_NEURONS
        # So we go from right to left so there can be an infinite amount of layers be drawn.
        start_x = constants.NN_GRAPH_START_POS_X
        # So we go from bottom to top so there can be an infinite of neurons drawn.
        start_y = constants.NN_GRAPH_START_POS_Y
        circle_size = constants.NN_GRAPH_CIRCLE_SIZE
        line_width = constants.NN_GRAPH_LINE_WIDTH

        # Create an array of the lines between the hidden layer and the output layer
        self.output_hidden_lines = []
        in_x = start_x - dist_between_layers
        out_x = start_x
        for line_num, line in enumerate(weights_hidden_output):
            in_y = start_y + dist_between_neurons * line_num
            output_hidden_line = []
            for entry_num, entry in enumerate(line):
                out_y = start_y + dist_between_neurons * entry_num
                output_hidden_line.append(pyglet.shapes.Line(
                    out_x, out_y, in_x, in_y, line_width, color=(47, 143, 191)))
            self.output_hidden_lines.append(output_hidden_line)

        # Create an array of lines between the input and hidden layer
        self.hidden_input_lines = []
        in_x = start_x - 2*dist_between_layers
        out_x = start_x - dist_between_layers
        for line_num, line in enumerate(weights_input_hidden):
            in_y = start_y + dist_between_neurons * line_num
            hidden_input_line = []
            for entry_num, entry in enumerate(line):
                out_y = start_y + dist_between_neurons * entry_num
                hidden_input_line.append(pyglet.shapes.Line(
                    out_x, out_y, in_x, in_y, line_width, color=(47, 143, 191)))
            self.hidden_input_lines.append(hidden_input_line)

        # Create a list of circles to represent the output neurons
        self.output_circles = []
        for i in range(self.output_num):
            self.output_circles.append(pyglet.shapes.Circle(
                start_x, start_y + i * dist_between_neurons, circle_size, color=(206, 55, 55)))

        # Create a list of circles to represent the hidden layer neurons
        self.hidden_circles = []
        for i in range(self.hidden_num):
            self.hidden_circles.append(pyglet.shapes.Circle(
                start_x - dist_between_layers, start_y + i * dist_between_neurons, circle_size, color=(206, 55, 55)))

        # Create a list of circles to represent the input neurons
        self.input_circles = []
        for i in range(self.input_num):
            self.input_circles.append(pyglet.shapes.Circle(
                start_x - 2*dist_between_layers, start_y + i * dist_between_neurons, circle_size, color=(206, 55, 55)))

    def draw(self, bird: flappy_bird):
        """
        Draw an updated version of the graph.

        Args:
            self (undefined):
            bird (flappy_bird): The bird from whom the NN shall be drawn.

        """
        NN = bird.NN

        # Update the opacity of the lines between the hidden and output layer and draw it
        for line_num, line in enumerate(NN.weights_hidden_output):
            for entry_num, entry in enumerate(line):
                self.output_hidden_lines[line_num][entry_num].opacity = 250 * entry
                self.output_hidden_lines[line_num][entry_num].draw()

        # Update the opacity of the lines between the input and hidden layer and draw it
        for line_num, line in enumerate(NN.weights_input_hidden):
            for entry_num, entry in enumerate(line):
                self.hidden_input_lines[line_num][entry_num].opacity = 250 * entry
                self.hidden_input_lines[line_num][entry_num].draw()

        # Update the opacity of the circles form the output and draw it
        for i, bias_value in enumerate(NN.bias_output[0]):
            self.output_circles[i].opacity = 250 * bias_value
            self.output_circles[i].draw()

        # Update the opacity of the circles of the hidden layer and draw it
        for i, bias_value in enumerate(NN.bias_hidden[0]):
            self.hidden_circles[i].opacity = 250 * bias_value
            self.hidden_circles[i].draw()

        for i in self.input_circles:
            i.draw()
