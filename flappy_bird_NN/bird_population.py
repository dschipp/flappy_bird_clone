import os, sys
path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(path)
__docformat__ = "google"

import pickle
from bird import flappy_bird
import constants
import pyglet
import logging


def check_collision(object_coordinates: list, block_coordinates: list) -> bool:
    """
    Check for the collision between an object and the blocks.

    Args:
        object_coordinates (list): [x, y, x + width, y + height]
        block_coordinates (list): [x_bot_left, y_bot_left, x_bot_right, y_bot_right, x_top_right, y_top_right, x_top_left, y_top_left]

    Returns:
        bool
        If the object is in collision with the blocks.

    """

    object_x_left = object_coordinates[0]  # x
    object_y_bot = object_coordinates[1]  # y
    object_x_right = object_coordinates[2]  # x + width
    object_y_top = object_coordinates[3]  # y + height

    block_x_bot_left = block_coordinates[0]  # x
    block_y_bot_left = block_coordinates[1]  # y + height
    block_x_bot_right = block_coordinates[2]  # x + width
    # block_y_bot_right = block_coordinates[3] # y + height

    block_x_top_right = block_coordinates[4]  # x + width
    block_y_top_right = block_coordinates[5]  # y
    block_x_top_left = block_coordinates[6]  # x
    # block_y_top_left = block_coordinates[7] # y

    # Check for the collision width the bottom block
    if object_x_left > block_x_bot_left and object_x_left < block_x_bot_right and object_y_bot < block_y_bot_left or object_x_right > block_x_bot_left and object_x_right < block_x_bot_right and object_y_bot < block_y_bot_left:
        return True

    # Check for collision with the top block
    if object_x_left > block_x_top_left and object_x_left < block_x_top_right and object_y_top > block_y_top_right or object_x_right > block_x_top_left and object_x_right < block_x_top_right and object_y_top > block_y_top_right:
        return True

    return False


class bird_population():
    def __init__(self, size: int, x_max: int, y_max: int) -> None:
        """
        Create a whole bird population.

        Args:
            self (undefined):
            size (int): The size of the population.
            x_max (int): The max x size / the width of the window.
            y_max (int): The max y size / height of the window.

        Returns:
            None

        """

        self.x_max = x_max
        self.y_max = y_max
        self.size = size

        self.birds = [flappy_bird(x=constants.BIRD_X, y=self.y_max/2)
                      for i in range(self.size)]

        self.best_bird_save_file_path = path + "/../best_bird.pickle"
        self.example_best_bird_save_file_path = path + "/../data/example_best_bird.pickle"

        self.hidden_circles = []
        self.output_circles = []
        self.input_circles = []
        self.hidden_input_lines = []
        self.output_hidden_lines = []
        self.init_NN_draw()

        self.NN_draw_blur_image = pyglet.image.load(path + "/../assets/menu_blur.png")
        self.NN_draw_blur_image.width = 170
        self.NN_draw_blur_image.height = 200
        self.NN_draw_blur = pyglet.sprite.Sprite(
            self.NN_draw_blur_image, x=450, y=25)

    def update(self, block_coordinates) -> bool:
        """
        Let the birds move and check if they hit something or else.

        Args:
            self (undefined):
            block_coordinates (undefined): [x_bot_left, y_bot_left, x_bot_right, y_bot_right, x_top_right, y_top_right, x_top_left, y_top_left]

        Returns:
            bool
            If all birds are dead.

        """

        all_birds_dead = True

        for bird in self.birds:

            if not bird.dead:
                bird.update(self.y_max)

            # Check for collision
            if check_collision([bird.x, bird.y, bird.x + bird.width, bird.y + bird.height], block_coordinates):
                bird.die()

            # Check if a bird passed a pipe
            if bird.nearest_block != block_coordinates[8] and not bird.dead and not block_coordinates[8] == 0:
                bird.add_score()
                # print("Got through one!")
            bird.nearest_block = block_coordinates[8]

            # Check if all birds are dead. If one bird is alive the game is not stopped
            if not bird.dead:
                all_birds_dead = False

        return all_birds_dead

    def learn(self, best_birds):
        """
        Let the birds learn from the best birds of a population.

        Args:
            self (undefined):
            best_birds (undefined): [score of the best bird, the list positions of the best bird]

        """

        logging.debug("Birds are learning from the " + str(len(best_birds)) + " best birds of the population.")

        steps = len(best_birds)
        for num, best_bird in enumerate(best_birds):
            lower_boundaries = round((num/steps) * len(self.birds))
            upper_boundaries = round(((num+1)/steps) * len(self.birds))
            for num, bird in enumerate(self.birds[lower_boundaries:upper_boundaries]):
                if num not in best_birds:
                    bird.learn_from_other_bird(self.birds[best_bird])
                    # Decrease the learning rate with increasing generations
                    bird.NN.learning_rate -= 0.00005
                    # bird.change_color((0, 255 * upper_boundaries, 255 * upper_boundaries))
                else:
                    pass
                    # bird.change_color((0, 0,255 * upper_boundaries))

    def birds_brain_decides(self, block_coordinates):
        """
        Let the NN of the birds decide what to do.

        Args:
            self (undefined):
            block_coordinates (undefined): [x_bot_left, y_bot_left, x_bot_right, y_bot_right, x_top_right, y_top_right, x_top_left, y_top_left]

        """

        for bird in self.birds:
            if not bird.dead:
                # Calculate the distances to the nearest pipe
                y_top = (bird.y - block_coordinates[7]) / self.y_max
                y_bot = (bird.y - block_coordinates[1]) / self.y_max
                dist_block = (bird.x - block_coordinates[2]) / self.x_max
                # y_bird = bird.y / y_max
                velocity_bird = (bird.velocity / 20) + 1

                # Ask the bird what he wants to do
                bird.decide_NN([y_top, y_bot, dist_block, velocity_bird])

    def check_best_bird(self) -> list:
        """
        Check for the best bird.

        Args:
            self (undefined):

        Returns:
            list: The score and the list positions of the best birds or None if all birds failed.
                    [score, [best_bird_list_pos]]

        """

        max_score = 0
        best_birds = []

        for bird in self.birds:
            if bird.score > max_score:
                max_score = bird.score

        for num, bird in enumerate(self.birds):
            if bird.score == max_score:
                best_birds.append(num)

        if max_score == 0:
            return None

        return [max_score, best_birds]

    def draw(self):
        """
        Draw the bird population. But not all of them.

        Args:
            self (undefined):

        """

        drawn_birds = 0  # Only draw a specific number of birds for better performance
        for bird in self.birds:
            if not bird.dead and drawn_birds < constants.DISPLAYED_BIRDS:
                bird.draw()
                self.draw_NN(bird)
                drawn_birds += 1

    def revive_population(self):
        """
        Revive all the birds.

        Args:
            self (undefined):

        """
        # Revive all birds
        for bird in self.birds:
            bird.revive(constants.JUMP_HEIGHT, self.y_max/2)

    def get_alive_count(self):
        """
        Get the number of still alive birds.

        Args:
            self (undefined):

        """
        count = 0
        for bird in self.birds:
            if not bird.dead:
                count += 1

        return count

    def recreate_population(self):
        """
        Create a new population of birds.

        Args:
            self (undefined):

        """
        self.birds = None
        self.birds = [flappy_bird(x=constants.BIRD_X, y=self.y_max/2)
                      for i in range(self.size)]

        logging.info("Created a new population of birds.")

    def save_best_bird(self):
        """
        Save the best bird of a generation.

        Args:
            self (undefined):

        """

        best_bird_list = self.check_best_bird()

        if best_bird_list is None:
            logging.warning("There is no best bird to save.")
            print("There is no best bird to save.")
            return

        best_bird_NN = self.birds[best_bird_list[1][0]].NN
        pickling_on = open(self.best_bird_save_file_path, "wb")
        pickle.dump(best_bird_NN, pickling_on)
        pickling_on.close()

        logging.info("Saved the best bird from this population.")
        print("Saved the best bird this population.")

    def load_best_bird(self):
        """
        Load the saved best bird and create a new generation from that bird.

        Args:
            self (undefined):

        """
        
        try:
            pickle_off = open(self.best_bird_save_file_path, "rb")
        except:
            pickle_off = open(self.example_best_bird_save_file_path, "rb")

        loaded_bird_NN = pickle.load(pickle_off)
        self.birds[0].NN = loaded_bird_NN
        pickle_off.close()

        logging.info("Loaded the saved best bird.")
        print("Loaded the saved best bird.")

        # self.learn([0,[0]])

    def init_NN_draw(self):

        NN = self.birds[0].NN
        
        dist_between_layers = 60
        dist_between_neurons = 40
        start_x = 640 - 40 # So we go from right to left so there can be an infinite amount of layers be drawn.
        start_y = 50 # So we go from bottom to top so there can be an infinite of neurons drawn.
        circle_size = 10
        line_width = 2

        # Draw the weights between output and hidden layer
        self.output_hidden_lines = []
        in_x = start_x - dist_between_layers
        out_x = start_x
        for line_num,line in enumerate(NN.weights_hidden_output):
            in_y = start_y + dist_between_neurons * line_num
            output_hidden_line = []
            for entry_num,entry in enumerate(line):
                out_y = start_y + dist_between_neurons * entry_num
                output_hidden_line.append(pyglet.shapes.Line(out_x, out_y, in_x, in_y, line_width, color = (47, 143, 191)))
            self.output_hidden_lines.append(output_hidden_line)

        # Draw the weights between hidden and input layer
        self.hidden_input_lines = []
        in_x = start_x - 2*dist_between_layers
        out_x = start_x - dist_between_layers
        for line_num,line in enumerate(NN.weights_input_hidden):
            in_y = start_y + dist_between_neurons * line_num
            hidden_input_line = []
            for entry_num,entry in enumerate(line):
                out_y = start_y + dist_between_neurons * entry_num
                hidden_input_line.append(pyglet.shapes.Line(out_x, out_y, in_x, in_y, line_width, color = (47, 143, 191)))
            self.hidden_input_lines.append(hidden_input_line)

        # Draw output neurons
        self.output_circles = []
        for i,bias_value in enumerate(NN.bias_output[0]):
            self.output_circles.append(pyglet.shapes.Circle(start_x, start_y + i * dist_between_neurons, circle_size, color =(206, 55, 55)))
            self.output_circles[-1].opacity = 250 * bias_value

        # Draw hidden neurons
        self.hidden_circles = []
        for i,bias_value in enumerate(NN.bias_hidden[0]):
            self.hidden_circles.append(pyglet.shapes.Circle(start_x - dist_between_layers, start_y + i * dist_between_neurons, circle_size, color =(206, 55, 55)))
            self.output_circles[-1].opacity = 250 * bias_value

        # Draw input neurons
        self.input_circles = []
        for i in range(NN.input_count):
            self.input_circles.append(pyglet.shapes.Circle(start_x - 2*dist_between_layers, start_y + i * dist_between_neurons, circle_size, color =(206, 55, 55)))

    def draw_NN(self, bird):

        NN = bird.NN

        # Draw the weights between output and hidden layer
        for line_num,line in enumerate(NN.weights_hidden_output):
            for entry_num,entry in enumerate(line):
                self.output_hidden_lines[line_num][entry_num].opacity = 250 * entry

        # Draw the weights between hidden and input layer
        for line_num,line in enumerate(NN.weights_input_hidden):
            for entry_num,entry in enumerate(line):
                self.hidden_input_lines[line_num][entry_num].opacity =  250 * entry

        # Draw output neurons
        for i,bias_value in enumerate(NN.bias_output[0]):
            self.output_circles[i].opacity = 250 * bias_value

        # Draw hidden neurons
        for i,bias_value in enumerate(NN.bias_hidden[0]):
            self.hidden_circles[i].opacity = 250 * bias_value

        self.NN_draw_blur.draw()

        for i in self.hidden_input_lines:
            for line in i:
                line.draw()
        
        for i in self.output_hidden_lines:
            for line in i:
                line.draw()

        for circle in self.hidden_circles:
            circle.draw()

        for circle in self.output_circles:
            circle.draw()

        for circle in self.input_circles:
            circle.draw()
        