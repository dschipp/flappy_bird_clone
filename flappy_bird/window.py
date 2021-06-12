import pyglet
from bird import flappy_bird
from blocks import blocks
from button import button

Y_TILING = 10
X_TILING = 16
BLOCK_WIDTH = 1.5
HOLE = 1.7
BLOCK_COUNT = 10
BLOCK_DIST = 4
SPEED = 1/200
BLOCK_SPEED = 0.06
BIRDSIZE = 15
JUMP_HIGHT = 2
GRAVITY = 0.23

BIRD_COUNT = 40


class app(pyglet.window.Window):

    def __init__(self) -> None:
        """
        Create the flappy bird window with blocks and bird.

        Args:
            self (undefined):

        Returns:
            None

        """
        super(app, self).__init__()

        self.y_scale = self.get_size()[0] / Y_TILING
        self.x_scale = self.get_size()[1] / X_TILING

        self.set_variables()

        pyglet.gl.glClearColor(255, 255, 255, 1.0)

        self.birds = [flappy_bird(x=50, y=Y_TILING/2 * self.y_scale, gravity=GRAVITY,
                                  jump_height=JUMP_HIGHT, radius=BIRDSIZE) for i in range(BIRD_COUNT)]

    def set_variables(self):
        """
        Set all the variables:
        - Crate all blocks
        - (Currently not) Create a / all birds
        - Set the starting point of the blocks
        - (WIP) Create a restart buttom, if the game ends
        - A variable if the game has already started

        Args:
            self (undefined):

        """
        self.startpoint = X_TILING / 2 + 3

        self.blocks = blocks(BLOCK_COUNT, BLOCK_DIST, BLOCK_WIDTH,
                             Y_TILING, HOLE, self.y_scale, self.x_scale, self.startpoint)

        # self.bird = bird(x=50, y=Y_TILING/2 * self.y_scale, gravity=GRAVITY, jump_height=JUMP_HIGHT,
        #                  radius=BIRDSIZE)

        self.started = False

        # self.restart_button = button(self.get_size()[1] / 2 ,self.get_size()[0] / 2, 600, 600)

    def update_app(self, timer):
        """
        Update the app and all the objects in that app:
        - The blocks
        - The bird

        Args:
            self (undefined):
            timer (undefined): The timer of the app.

        """
        self.clear()

        self.blocks.update(BLOCK_SPEED)

        # self.bird.update(self.get_size()[0])

        for bird in self.birds:
            bird.update(self.get_size()[0])

        # Multiply with a factor so it feels better
        for bird in self.birds:
            if self.blocks.check_collision(bird.x, bird.y, bird.radius * 0.8):
                bird.die()

        # Calculate the nearest blocks and normalize them
        x_max = self.get_size()[1]
        y_max = self.get_size()[0]

        # [x_bot_left, y_bot_left, x_bot_right, y_top_right, x_top_right, y_top_right, x_top_left, y_top_left]

        stop_game = True

        for bird in self.birds:

            block_coordinates = self.blocks.nearest_block_coordinates(bird.x)

            if block_coordinates[2] - bird.x < 0:
                bird.add_score()

            dist_top_block = abs(bird.y - block_coordinates[7]) / y_max
            dist_bot_block = abs(bird.y - block_coordinates[1]) / y_max
            dist_block = abs(bird.x - block_coordinates[0]) / x_max

            bird.decide_NN([dist_top_block, dist_bot_block, dist_block])

            if not bird.dead:
                stop_game = False

        if stop_game:
            self.restart()

            i = 0
            for bird in self.birds:
                i += bird.score

            if i == 0:
                self.birds = [flappy_bird(x=50, y=Y_TILING/2 * self.y_scale, gravity=GRAVITY,
                                          jump_height=JUMP_HIGHT, radius=BIRDSIZE) for i in range(BIRD_COUNT)]

    def on_draw(self):
        """
        Draw all the objects in the app:
        - The blocks
        - The bird / birds

        Args:
            self (undefined):

        """
        self.clear()

        self.blocks.draw()
        # self.bird.draw()

        for bird in self.birds:
            bird.draw()

    def pause(self):
        """
        Pause the game and:
        - (WIP) Draw the restart buttom to restart the game.

        Args:
            self (undefined):

        """
        # self.restart_button.draw()

        pyglet.clock.unschedule(self.update_app)

    def restart(self):
        """
        (WIP) Restart the whole game.

        Args:
            self (undefined):

        TODO: Implement a working function.

        """
        self.pause()

        self.set_variables()

        self.blocks = blocks(BLOCK_COUNT, BLOCK_DIST, BLOCK_WIDTH,
                             Y_TILING, HOLE, self.y_scale, self.x_scale, self.startpoint)

        self.started = False

        for bird in self.birds:
            bird.revive(JUMP_HIGHT, Y_TILING/2 * self.y_scale)

        pyglet.clock.schedule_interval(self.update_app, SPEED)

    def on_key_press(self, symbol, modifiers):
        """
        The function to check keyboard inputs and react to them.

        Args:
            self (undefined):
            symbol (undefined):
            modifiers (undefined):

        """
        if symbol == pyglet.window.key.UP or symbol == pyglet.window.key.SPACE:
            if not self.started:
                pyglet.clock.schedule_interval(self.update_app, SPEED)
                self.started = True
            # self.bird.move_up()
        if symbol == pyglet.window.key.ESCAPE:
            self.close()
