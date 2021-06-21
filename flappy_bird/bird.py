import pyglet
from pyglet import sprite
from NN import Neural_Net
from NN_functions import decision_function

# FIXME: The hitbox is weird with the new images

class flappy_bird(sprite.Sprite):
    def __init__(self, x: int, y: int, radius: int, gravity: int, jump_height: int, color: tuple = (0, 128, 255)) -> None:
        """
        Create a bird, potentially a bird with a Neural Network learning. Currently it is just a circle.

        Args:
            self (undefined):
            x (int): The x starting Coordinate
            y (int): The y starting Coordinate
            radius (int): The Radius Size of the Bird
            gravity (int): The gravity which the bird is falling
            jump_height (int): The height the bird jumps
            color (tuple=(50,225,30)): The Color the circle of the bird has. Currently some kind of blue

        Returns:
            None

        """
        # load the image
        bird_image = pyglet.image.load("./assets/flappy_bird.png")

        # Initialise the upper function.
        super(flappy_bird, self).__init__(bird_image, x=x, y=y)
        self.scale = radius / bird_image.width
        self.radius = radius

        self.gravity = -gravity
        self.velocity = 0
        self.jump_height = jump_height
        	
        self.dead = False
        self.score = 0

        self.nearest_block = 0 # Safe the number of the nearest block to check the score

        self.NN = Neural_Net(4, 2)  # Crate a Neural Network for this bird.

        self.died_with_outputs = [] # A list to save the outputs the NN gave when the bird died
        self.died_with_inputs = [] # A list to save the inputs the NN gave when the bird died

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
        if self.y >= height - self.radius * 7:
            self.y = height - self.radius * 7
            self.velocity = 0

        if self.y <= self.radius:
            self.y = self.radius
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
