import pyglet
import random
from pyglet import shapes
from bird import bird
from blocks import blocks

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
# TODO: Colision detection
# TODO: Top and bottom Barriers

    def __init__(self) -> None:
        super(app, self).__init__()

        self.y_scale = self.get_size()[0] / Y_TILING
        self.x_scale = self.get_size()[1] / X_TILING

        self.startpoint = X_TILING / 2 + 3

        self.blocks = blocks(BLOCK_COUNT, BLOCK_DIST, BLOCK_WIDTH,
                             Y_TILING, HOLE, self.y_scale, self.x_scale, self.startpoint)

        self.bird = bird(x=50, y=Y_TILING/2 * self.y_scale,
                         radius=BIRDSIZE, color=(50, 225, 30))

        pyglet.gl.glClearColor(255, 255, 255, 1.0)

    def update_app(self, timer):
        self.clear()

        self.blocks.update(BLOCK_SPEED)

        self.bird.move()

    def on_draw(self):
        self.clear()

        self.blocks.draw()

        self.bird.draw()

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.UP:
            self.bird.move_up()
        elif symbol == pyglet.window.key.DOWN:
            pyglet.clock.schedule_interval(self.update_app, SPEED)
