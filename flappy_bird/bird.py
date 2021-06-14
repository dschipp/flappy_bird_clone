import pyglet
from pyglet import shapes
from NN import Neural_Net


class flappy_bird(shapes.Circle):
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

        TODO: Use a picture of the bird not just a circle.

        """

        # Initialise the upper function.
        super(flappy_bird, self).__init__(x=x, y=y, radius=radius, color=color)

        self.gravity = -gravity
        self.velocity = 0
        self.jump_height = jump_height

        self.dead = False
        self.score = 0

        self.nearest_block = 0

        self.NN = Neural_Net(3, 1)  # Crate a Neural Network for this bird.

    def move_up(self):
        """
        Let's the bird jumps.

        Args:
            self (undefined):

        """
        self.velocity += self.jump_height

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
        # TODO: Implement a learning function for the bird and the Neuronal Net
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
        
        # Check if the bird is dead
        if self.dead:
            return

        decision = self.NN.calc_outputs(distances)

        # print(decision)

        if decision[0] > 0.5:
            self.move_up()
