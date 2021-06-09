import pyglet
from pyglet import shapes
from NN import Neural_Net


class bird(shapes.Circle):
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
        super(bird, self).__init__(x=x, y=y, radius=radius, color=color)

        self.gravity = -gravity
        self.velocity = 0
        self.jump_height = jump_height

        # self.NN = Neural_Net(9, 1)  # Crate a Neural Network for this bird.

    def move_up(self):
        """
        Let's the bird jumps.

        Args:
            self (undefined):

        """
        self.velocity += self.jump_height

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

        if self.y <= self.radius / 2:
            self.y = self.radius / 2
            self.velocity = 0

    def decide_NN(self, corner_positions: list) -> bool:
        """
        A function to determine what the Neural Net of the bird should do. Jump of no Jump.

        Args:
            self (undefined):
            corner_positions (undefined): The corner positions of the next Block pair.

        Returns:
            If the bird should jump or not as a boolean.

        """

        corner_positions.append(self.x)

        decision = self.NN.output(corner_positions)

        print(decision)
