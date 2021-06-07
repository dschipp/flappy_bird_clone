import pyglet
from pyglet import shapes
import random


class block(shapes.Rectangle):
    def __init__(self, x, y, width, height, color=(0, 153, 76)):
        super(block, self).__init__(
            x=x, y=y, width=width, height=height, color=color)


class blocks():
    def __init__(self, count, block_dist, block_width, y_tiling, hole, y_scale, x_scale, startpoint):

        self.blocks = list()

        self.x_scale = x_scale
        self.y_scale = y_scale
        self.count = count
        self.block_width = block_width
        self.block_dist = block_dist

        for block_pair_count in range(count):
            height = random.randint(2, 5)

            for block_count in range(2):
                block_pair = [
                    block(x=(block_pair_count + block_dist * block_pair_count + startpoint) * x_scale,
                          y=0, width=x_scale * block_width, height=y_scale * height),
                    block(x=(block_pair_count + block_dist * block_pair_count + startpoint) * x_scale, y=y_scale * (
                        height+hole), width=x_scale * block_width, height=y_scale * (y_tiling-height))
                ]

            self.blocks.append(block_pair)

    def update(self, BLOCK_SPEED):

        for block_pair in self.blocks:
            for block in block_pair:
                if block.x < - self.block_width * self.x_scale:
                    block.x = (self.count + self.block_dist *
                               self.count) * self.x_scale
                block.x -= BLOCK_SPEED * self.x_scale

    def draw(self):
        for block_pair in self.blocks:
            for block in block_pair:
                block.draw()
