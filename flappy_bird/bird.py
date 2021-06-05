import pyglet
from pyglet import shapes

JUMP_HIGHT = 10
GRAVITY = 0.3


class bird(shapes.Circle):
    def __init__(self, x, y, radius, color) -> None:
        super(bird, self).__init__(x=x, y=y, radius=radius, color=color)

        self.gravity = -GRAVITY
        self.velocity = 0

    def move_up(self):
        self.velocity += JUMP_HIGHT

    def move(self):
        self.velocity += self.gravity
        self.y += self.velocity
