import os, sys
path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(path)

import pickle
from bird import flappy_bird
import constants
import pyglet


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

        self.best_bird_save_file_path = "best_bird.pickle"
        self.example_best_bird_save_file_path = "data/example_best_bird.pickle"

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

    def save_best_bird(self):
        """
        Save the best bird of a generation.

        Args:
            self (undefined):

        """

        best_bird_list = self.check_best_bird()

        if best_bird_list is None:
            print("There is no best bird to save.")
            return

        best_bird_NN = self.birds[best_bird_list[1][0]].NN
        pickling_on = open(self.best_bird_save_file_path, "wb")
        pickle.dump(best_bird_NN, pickling_on)
        pickling_on.close()

        print("Saved the best bird this population.")

    def load_best_bird(self):
        """
        Load the saved best bird and create a new generation from that bird.

        Args:
            self (undefined):

        """
        pass # TODO: Something doesnt work here
#        try:
#            pickle_off = open(self.best_bird_save_file_path, "rb")
#        except:
#            pickle_off = open(self.example_best_bird_save_file_path, "rb")

#        loaded_bird_NN = pickle.load(pickle_off)
#        self.birds[0].NN = loaded_bird_NN
#        pickle_off.close()

#        print("Loaded the saved best bird.")

        # self.learn([0,[0]])
