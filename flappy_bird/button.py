import os, sys
path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(path)

"""
Implement a Button class to create Button with a text written on it.
"""

import pyglet
from pyglet import shapes

class button:
    def __init__(self, x, y, width, height):
        self.box = shapes.Rectangle(x = x, y = y, width =width, height = height, color=(0, 153, 76))

    def draw(self):
        self.box.draw()