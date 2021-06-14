import pyglet
from pyglet import shapes
import random


class block(shapes.Rectangle):
    def __init__(self, x: int, y: int, width: int, height: int, color=(0, 153, 76)):
        """
        Create a block / Rectangle.

        Args:
            self (undefined):
            x (int): The x Position of the Block / The x of the lower left corner of the block.
            y (int): The y Position of the Block / The y of the lower left corner of the block.
            width (int): The width of the block / So the x coordinate + the width => lower right corner.
            height (int): The height of the block / So the y coordinate + the height => upper left corneer.
            color=(0 (,153,76)): The color of the block. Standard some kind of green.

        """
        super(block, self).__init__(
            x=x, y=y, width=width, height=height, color=color)

        self.height = height
        self.width = width


class blocks():
    def __init__(self, count: int, block_dist: int, block_width: int, y_tiling: int, hole: int, y_scale: int, x_scale: int, startpoint: int) -> None:
        """
        Create an list of block pairs one at the top and the other at the bottom with a distance between them.

        Args:
            self (undefined):
            count (int): The number of block pairs.
            block_dist (int): The distance between the block pairs.
            block_width (int): The width of the blocks.
            y_tiling (int): In how many tiles the y is splittet up.
            hole (int): The size of the hole between the blocks in the block pair. So between the upper and lower block.
            y_scale (int): The y scale of the window, because of the tiling.
            x_scale (int): The x scale of the window after the tiling
            startpoint (int): The x start coordinate of the first block pair.

        Returns:
            None

        TODO: Rewrite the tiling of the window, it is not really usefull.

        """

        self.blocks = list()

        self.x_scale = x_scale
        self.y_scale = y_scale
        self.count = count
        self.block_width = block_width
        self.block_dist = block_dist

        # Create a list of block pairs with random heights. The list contains of block pairs, where the firs block
        # is the bottom block and the second one is the top block
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
        Update the position of the block pairs.

        Args:
            self (undefined):
            speed (undefined): The speed with which the block pairs are moving.

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

    def nearest_block_coordinates(self, x: int, x_max: int = 500) -> list:
        """
        Check from given x coordinate which block pair ist the nearest.
        [x_bot_left, y_bot_left, x_bot_right, y_top_right, x_top_right, y_top_right, x_top_left, y_top_left]

        Args:
            self (undefined):
            x (int): The x coordinate to check.
            x_max=500 (int): The maximum x value of the window. So basically the window x size.

        Returns:
            list. A List of the cornder coordinates from the hole between the block pairs.

        """

        nearest_block = 0
        x_before = x_max

        for block_count, block_pair in enumerate(self.blocks):
            for block in block_pair:

                if block.x - x + block.width > 0 and block.x - x + block.width <= x_before:
                    nearest_block = block_count  # Notice the list position of the nearest block
                    # Change the block color of the nearest block to check.
                    block.color = (200, 0, 0)
                    x_before = block.x - x + block.width
                else:
                    block.color = (0, 153, 76)

        block_pair = self.blocks[nearest_block]

        # Draw the corners as little circles

        # shapes.Circle(x=block_pair[0].x, y=block_pair[0].y +
        #               block_pair[0].height, radius=5, color=(100, 0, 0)).draw()
        # shapes.Circle(x=block_pair[0].x + block_pair[0].width, y=block_pair[0].y +
        #               block_pair[0].height, radius=5, color=(100, 0, 0)).draw()

        # shapes.Circle(x=block_pair[1].x + block_pair[1].width,
        #               y=block_pair[1].y, radius=5, color=(100, 0, 0)).draw()
        # shapes.Circle(x=block_pair[1].x, y=block_pair[1].y,
        #               radius=5, color=(100, 0, 0)).draw()

        corner_array = [block_pair[0].x, block_pair[0].y + block_pair[0].height,
                        block_pair[0].x + block_pair[0].width, block_pair[0].y +
                        block_pair[0].height,
                        block_pair[1].x + block_pair[1].width, block_pair[1].y,
                        block_pair[1].x, block_pair[1].y, nearest_block]

        return corner_array

    def draw(self):
        """
        Draw all blocks pairs.

        Args:
            self (undefined):

        """
        for block_pair in self.blocks:
            for block in block_pair:
                block.draw()
