import pyglet
from pyglet import shapes

class button:
    def __init__(self, x, y, width, height):
        self.box = shapes.Rectangle(x = x, y = y, width =width, height = height, color=(0, 153, 76))

    def draw(self):
        self.box.draw()