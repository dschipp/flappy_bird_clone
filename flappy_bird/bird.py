import pyglet
from pyglet import sprite
from NN import Neural_Net
import constants

# RGB colors of the beak: R = 96.1; G = 30.2; B = 5.5


def decision_function(input):
    """
    The function after what the bird decides what to do.

    Args:
        input (undefined): The Input List

    """
    if input[1] >= input[0]:
        return True
    return False


class flappy_bird(sprite.Sprite):
    def __init__(self, x: int, y: int, color: tuple = (0, 128, 255)) -> None:
        """
        Create a flappy bird with a working Neural Network.

        Args:
            self (undefined):
            x (int): The x position of the Bird.
            y (int): The y position of the bird.
            color (tuple=(0,128,255)): (WIP) The color of the bird.

        Returns:
            None

        """
        # load the image
        bird_image = pyglet.image.load("./assets/flappy_bird.png")

        # Initialise the upper function.
        super(flappy_bird, self).__init__(bird_image, x=x, y=y)
        self.scale = constants.BIRD_SIZE / bird_image.width
        self.radius = constants.BIRD_SIZE

        self.gravity = -constants.GRAVITY
        self.velocity = 0
        self.jump_height = constants.JUMP_HEIGHT

        self.dead = False
        self.score = 0

        self.nearest_block = 0  # Safe the number of the nearest block to check the score

        self.recreate_NN()

        # A list to save the outputs the NN gave when the bird died
        self.died_with_outputs = []
        self.died_with_inputs = []  # A list to save the inputs the NN gave when the bird died

    def recreate_NN(self):
        """
        Create a new Neural Network / Brain of the Bird.

        Args:
            self (undefined):

        """
        self.NN = Neural_Net(4, 2)  # Crate a Neural Network for this bird.

    def move_up(self):
        """
        Let's the bird jumps.

        Args:
            self (undefined):

        """
        self.velocity += self.jump_height

    def change_color(self, color):
        self.color = color

    def add_score(self):
        """
        Add one to the bird score

        Args:
            self (undefined):

        """
        self.score += 1

    def update(self, height: int):
        """
        Update the position of the bird.

        Args:
            self (undefined):
            height (int): The maximum height of the window.

        """

        self.velocity += self.gravity
        self.y += self.velocity

        # TODO: Tilt the birds upwards or downwards
        # self.rotation =  90 * abs(self.velocity) / 15 - 45

        # Check if the bird hits the boundaries of the window / playing field.
        if self.y >= height - self.height * 8:
            self.y = height - self.height * 8
            self.velocity = 0

        if self.y <= self.height * 2:
            self.y = self.height * 2
            self.velocity = 0

    def die(self):
        """
        Let the bird die => He cant jump anymore.

        Args:
            self (undefined):

        """
        self.jump_height = 0
        self.dead = True
        self.nearest_block = 0

    def learn_from_other_bird(self, learn_bird):
        """
        Let the NN of the bird adapt from another bird.

        Args:
            self (undefined):
            learn_bird (undefined): The bird that should be learned from

        """
        self.NN.adapting(learn_bird.NN)

    def revive(self, jump_height: int, y_pos: int):
        """
        Let the bird revive.

        Args:
            self (undefined):
            jump_height (int): The jump height of the bird.
            y_pos (int): The starting x pos.

        """

        self.jump_height = jump_height
        self.dead = False
        self.y = y_pos
        self.score = 0

    def decide_NN(self, distances: list, max_x: int = 1) -> bool:
        """
        A function to determine what the Neural Net of the bird should do. Jump of no Jump.

        Args:
            self (undefined):
            distances (undefined): Distances / inputs for the NN

        Returns:
            If the bird should jump or not as a boolean.

        """

        decision = self.NN.calc_outputs(distances)
        self.died_with_outputs = decision

        if decision_function(decision):
            self.move_up()
