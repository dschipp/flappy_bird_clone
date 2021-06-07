import pyglet
from pyglet import shapes
import random


class block(shapes.Rectangle):
    def __init__(self, x: int, y: int, width: int, height: int, color=(0, 153, 76)):
        """
        Description of __init__

        Args:
            self (undefined):
            x (int):
            y (int):
            width (int):
            height (int):
            color=(0 (,153,76)):

        """
        super(block, self).__init__(
            x=x, y=y, width=width, height=height, color=color)


class blocks():
    def __init__(self, count: int, block_dist: int, block_width: int, y_tiling: int, hole: int, y_scale: int, x_scale: int, startpoint: int) -> None:
        """
        Description of __init__

        Args:
            self (undefined):
            count (int):
            block_dist (int):
            block_width (int):
            y_tiling (int):
            hole (int):
            y_scale (int):
            x_scale (int):
            startpoint (int):

        Returns:
            None

        """

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
                          y=0, width=x_scale * block_width, height=y_scale * height),  # Bottom Block
                    block(x=(block_pair_count + block_dist * block_pair_count + startpoint) * x_scale, y=y_scale * (
                        height+hole), width=x_scale * block_width, height=y_scale * (y_tiling-height))  # Top Block
                ]

            self.blocks.append(block_pair)

    def update(self, speed):
        """
        Description of update

        Args:
            self (undefined):
            speed (undefined):

        """

        for block_pair in self.blocks:
            for block in block_pair:
                if block.x < - self.block_width * self.x_scale:
                    block.x = (self.count + self.block_dist *
                               self.count) * self.x_scale
                block.x -= speed * self.x_scale

    def check_collision(self, x: int, y: int, radius: int = 0) -> bool:
        """
        Description of check_collision. Check if the given Coordinates hit a Block.

        Args:
            self (undefined):
            x (int): The x Coordinate of the object to check
            y (int): The y Coordinate of the object to check
            radius (int=0): The Radius of the object to check

        Returns: If the object hits
            bool

        """

        for block_pair in self.blocks:
            for top, block in enumerate(block_pair):

                top_bottom = 1  # Var to determine if the radius should be added or subtracted
                if not top:
                    top_bottom = -1

                if x + radius > block.x and x + radius < block.x + block.width and y + top_bottom * radius > block.y and y + top_bottom * radius < block.y + block.height:
                    return True

    def draw(self):
        """
        Description of draw

        Args:
            self (undefined):

        """
        for block_pair in self.blocks:
            for block in block_pair:
                block.draw()
