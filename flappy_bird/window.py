import pyglet
from bird import flappy_bird
from blocks import blocks
from button import button

Y_TILING = 10
X_TILING = 16
BLOCK_WIDTH = 1.5
HOLE = 2
BLOCK_COUNT = 4
BLOCK_DIST = 6
SPEED = 1/200
BLOCK_SPEED = 0.04
BIRDSIZE = 15
JUMP_HIGHT = 5
GRAVITY = 0.2

NN_DECISION_SPEED = 0.1
BIRD_COUNT = 200


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

        # Get the max x and y values for normalisation
        x_max = self.get_size()[1]
        y_max = self.get_size()[0]

        stop_game = True  # Variable to check if the game should be stopped because all birds are dead

        # [x_bot_left, y_bot_left, x_bot_right, y_top_right, x_top_right, y_top_right, x_top_left, y_top_left, block_number]
        block_coordinates = self.blocks.nearest_block_coordinates(self.birds[0].x)

        for bird in self.birds:
            
            if not bird.dead:
                bird.update(self.get_size()[0])
            
            # Check for collision
            if self.blocks.check_collision(bird.x, bird.y, bird.radius * 0.8): # Multiply with a factor so it feels better
                bird.die()

            if bird.nearest_block != block_coordinates[8] and not bird.dead: # Check if a bird passed a pipe
                bird.add_score()
                # print("Got through one!")
                bird.nearest_block = block_coordinates[8]

            # Check if all birds are dead. If one bird is alive the game is not stopped
            if not bird.dead:
                stop_game = False

        # If all birds are dead the game is get restarted and if no bird passed a single pipe a new population of birds is created
        if stop_game:
            # Check the score
            best_bird = self.check_best_bird()

            # If the score is 0, create a new population
            if best_bird == -1:
                print("No one made it :(")
                self.birds = [flappy_bird(x=50, y=Y_TILING/2 * self.y_scale, gravity=GRAVITY,
                                          jump_height=JUMP_HIGHT, radius=BIRDSIZE) for i in range(BIRD_COUNT)]
            else:
                print("Birds are learning...")
                for num, bird in enumerate(self.birds):
                    if num != best_bird:
                        bird.learn_from_other_bird(self.birds[best_bird])
                        bird.best_bird = False
                    else:
                        bird.best_bird = True
            
            # Restart the game
            self.restart()

    def bird_decisions(self, timer):
        """
        A explicit function to let the birds decide an and don't do that in every step of the update.

        Args:
            self (undefined):
            timer (undefined):

        """
    
        x_max = self.get_size()[1]
        y_max = self.get_size()[0]

        block_coordinates = self.blocks.nearest_block_coordinates(self.birds[0].x)
        self.blocks.change_color(block_coordinates[8])

        for bird in self.birds:
            if not bird.dead:
                # Calculate the distances to the nearest pipe
                y_top = block_coordinates[7] / y_max
                y_bot = block_coordinates[1] / y_max
                dist_block = abs(bird.x - block_coordinates[2]) / x_max
                y_bird = bird.y / y_max

                # Ask the bird what he wants to do
                bird.decide_NN([y_top, y_bot, dist_block, y_bird])

    def check_best_bird(self) -> int:
        """
        Check for the best bird.

        Args:
            self (undefined):

        Returns:
            int: The position of the best bird or -1 if all birds failed.

        """
        
        max_score = 0
        best_bird = 0

        for num, bird in enumerate(self.birds):
            if bird.score > max_score:
                max_score = bird.score
                best_bird = num

        if max_score == 0:
            return -1

        print("The score of the best bird was: " + str(max_score))
        print("The best bird was number: " + str(best_bird))
        return best_bird

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
        
        for bird in self.birds:
            if not bird.dead:
                bird.draw()

        # self.birds[self.check_best_bird()].draw()

    def pause(self):
        """
        Pause the game and:
        - (WIP) Draw the restart buttom to restart the game.

        Args:
            self (undefined):

        """
        # self.restart_button.draw()

        pyglet.clock.unschedule(self.update_app)
        pyglet.clock.unschedule(self.bird_decisions)

    def restart(self):
        """
        Restart the whole game.

        Args:
            self (undefined):

        """
        # First pause the game. FIXME: If the game is already stopped, this could lead to errors in the future.
        self.pause()

        self.set_variables()

        self.blocks = blocks(BLOCK_COUNT, BLOCK_DIST, BLOCK_WIDTH,
                             Y_TILING, HOLE, self.y_scale, self.x_scale, self.startpoint)

        self.started = False
        
        # Revive all birds
        for bird in self.birds:
            bird.revive(JUMP_HIGHT, Y_TILING/2 * self.y_scale)

        print("Restarting with a new generation. \n")
        pyglet.clock.schedule_interval(self.update_app, SPEED)
        pyglet.clock.schedule_interval(self.bird_decisions, NN_DECISION_SPEED)

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
                pyglet.clock.schedule_interval(self.bird_decisions, NN_DECISION_SPEED)
                self.started = True
            #self.birds[1].move_up()
        if symbol == pyglet.window.key.ESCAPE:
            self.close()
