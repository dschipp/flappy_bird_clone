import pyglet
import random
from pyglet import shapes
from bird import bird

Y_TILING = 10
X_TILING = 16
BLOCK_WIDTH = 1.3
HOLE = 2
BLOCK_COUNT = 10
BLOCK_DIST = 3.5
SPEED = 1/200
BLOCK_SPEED = 0.04
BIRDSIZE = 20


class app(pyglet.window.Window):

    def __init__(self) -> None:
        super(app, self).__init__()

        self.y_scale = self.get_size()[0] / Y_TILING
        self.x_scale = self.get_size()[1] / X_TILING

        self.startpoint = X_TILING / 2 + 3

        self.blocks = list()
        self.create_blocks()

        self.bird = bird(x=50, y=Y_TILING/2 * self.y_scale,
                         radius=BIRDSIZE, color=(50, 225, 30))

        pyglet.gl.glClearColor(255, 255, 255, 1.0)
        pyglet.clock.schedule_interval(self.update_app, SPEED)

    def create_blocks(self):
        for block_pair_count in range(BLOCK_COUNT):
            height = random.randint(2, 5)

            for block_count in range(2):
                block_pair = [
                    shapes.Rectangle(x=(block_pair_count + BLOCK_DIST * block_pair_count + self.startpoint) * self.x_scale,
                                     y=0, width=self.x_scale * BLOCK_WIDTH, height=self.y_scale * height, color=(0, 153, 76)),
                    shapes.Rectangle(x=(block_pair_count + BLOCK_DIST * block_pair_count + self.startpoint) * self.x_scale, y=self.y_scale * (
                        height+HOLE), width=self.x_scale * BLOCK_WIDTH, height=self.y_scale * (Y_TILING-height), color=(0, 153, 76))
                ]

            self.blocks.append(block_pair)

    def update_app(self, timer):
        self.clear()

        for block_pair in self.blocks:
            for block in block_pair:
                if block.x < - BLOCK_WIDTH * self.x_scale:
                    block.x = (BLOCK_COUNT + BLOCK_DIST *
                               BLOCK_COUNT) * self.x_scale
                block.x -= BLOCK_SPEED * self.x_scale

        self.bird.move()

    def on_draw(self):
        self.clear()

        for block_pair in self.blocks:
            for block in block_pair:
                block.draw()

        self.bird.draw()

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.UP:
            self.bird.move_up()
