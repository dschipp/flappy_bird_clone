import pyglet
import random
from pyglet import shapes
from bird import bird
from blocks import blocks

Y_TILING = 10
X_TILING = 16
BLOCK_WIDTH = 1.5
HOLE = 1.5
BLOCK_COUNT = 10
BLOCK_DIST = 4
SPEED = 1/200
BLOCK_SPEED = 0.04
BIRDSIZE = 15
JUMP_HIGHT = 9
GRAVITY = 0.25

class app(pyglet.window.Window):

    def __init__(self) -> None:
        super(app, self).__init__()

        self.y_scale = self.get_size()[0] / Y_TILING
        self.x_scale = self.get_size()[1] / X_TILING

        self.startpoint = X_TILING / 2 + 3

        self.blocks = blocks(BLOCK_COUNT, BLOCK_DIST, BLOCK_WIDTH,
                             Y_TILING, HOLE, self.y_scale, self.x_scale, self.startpoint)

        self.bird = bird(x=50, y=Y_TILING/2 * self.y_scale, gravity=GRAVITY, jump_height=JUMP_HIGHT,
                         radius=BIRDSIZE)

        self.started = False

        pyglet.gl.glClearColor(255, 255, 255, 1.0)

    def update_app(self, timer):
        self.clear()

        self.blocks.update(BLOCK_SPEED)

        self.bird.update(self.get_size()[0])

        if self.blocks.check_collision(self.bird.x, self.bird.y, self.bird.radius * 0.8): # Multiply with a factor so it feels better
            pyglet.clock.unschedule(self.update_app)

    def on_draw(self):
        self.clear()

        self.blocks.draw()
        self.bird.draw()
    
    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.UP or symbol == pyglet.window.key.SPACE:
            if not self.started:
                pyglet.clock.schedule_interval(self.update_app, SPEED)
                self.started = True
            self.bird.move_up(self.get_size()[0])
        if symbol == pyglet.window.key.ESCAPE:
            self.close()
