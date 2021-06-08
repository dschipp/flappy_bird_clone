import pyglet
import random
from pyglet import shapes
from bird import bird
from blocks import blocks
from button import button
from NN import Neural_Net

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

        self.set_variables()

        pyglet.gl.glClearColor(255, 255, 255, 1.0)

        self.NN = Neural_Net(4, 1) # Init the Neural Net
        #pyglet.clock.schedule_interval(self.NN_decides, 0.1)

    def NN_decides(self):
        pass
    
    def set_variables(self):
        self.startpoint = X_TILING / 2 + 3

        self.blocks = blocks(BLOCK_COUNT, BLOCK_DIST, BLOCK_WIDTH,
                             Y_TILING, HOLE, self.y_scale, self.x_scale, self.startpoint)

        self.bird = bird(x=50, y=Y_TILING/2 * self.y_scale, gravity=GRAVITY, jump_height=JUMP_HIGHT,
                         radius=BIRDSIZE)
        
        self.started = False

        self.restart_button = button(self.get_size()[1] / 2 ,self.get_size()[0] / 2, 600, 600)

    def update_app(self, timer):
        self.clear()

        self.blocks.update(BLOCK_SPEED)

        self.bird.update(self.get_size()[0])

        if self.blocks.check_collision(self.bird.x, self.bird.y, self.bird.radius * 0.8): # Multiply with a factor so it feels better
            self.pause()

        self.blocks.nearest_block_coordinates(self.bird.x)

    def on_draw(self):
        self.clear()

        self.blocks.draw()
        self.bird.draw()
    
    def pause(self):
        self.restart_button.draw()

        pyglet.clock.unschedule(self.update_app)

    def restart(self):
        self.set_variables()
    
    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.UP or symbol == pyglet.window.key.SPACE:
            if not self.started:
                pyglet.clock.schedule_interval(self.update_app, SPEED)
                self.started = True
            self.bird.move_up(self.get_size()[0])
        if symbol == pyglet.window.key.ESCAPE:
            self.close()
