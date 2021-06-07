import pyglet
from pyglet import shapes


class bird(shapes.Circle):
    def __init__(self, x: int, y: int, radius: int, gravity: int, jump_height: int, color: tuple = (50, 225, 30)) -> None:
        """
        Description of __init__

        Args:
            self (undefined):
            x (int):
            y (int):
            radius (int):
            gravity (int):
            jump_height (int):
            color (tuple=(50,225,30)):

        Returns:
            None

        """
    
        super(bird, self).__init__(x=x, y=y, radius=radius, color=color)

        self.gravity = -gravity
        self.velocity = 0
        self.jump_height = jump_height

    def move_up(self, y):
        """
        Description of move_up

        Args:
            self (undefined):

        """
        self.velocity += self.jump_height

    def update(self, x, y):
        """
        Description of move

        Args:
            self (undefined):

        """
        if self.y < y - self.radius * 2 and self.y > 0:
            self.velocity += self.gravity
            self.y += self.velocity
