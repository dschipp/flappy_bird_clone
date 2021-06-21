import pyglet
from bird import flappy_bird
from blocks import blocks
from button import button

BLOCK_WIDTH = 40
HOLE = 120
BLOCK_COUNT = 4
BLOCK_DIST = 150
SPEED = 1/200
BLOCK_SPEED = 1
BIRDSIZE = 30
JUMP_HIGHT = 5
GRAVITY = 0.2

NN_DECISION_SPEED = 0.1
BIRD_COUNT = 100


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

        self.y_max = self.get_size()[0]
        self.x_max = self.get_size()[1]

        self.set_variables()

        # Draw the background
        self.background_image = pyglet.image.load("./assets/background.png")
        self.background = pyglet.sprite.Sprite(
            self.background_image, x=0, y=-20)

        # Create the Scoretext / Scoreboard
        self.max_score = 0
        self.score_text = pyglet.text.Label('Score : 0',
                          font_name='Times New Roman',
                          font_size=25, color = (0,0,0, 255),
                          x=self.x_max * 40/41, y=self.y_max* 2/3)

        # Create the birds
        self.birds = [flappy_bird(x=50, y=self.y_max/2, gravity=GRAVITY,
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
        self.startpoint = BLOCK_DIST  # X_TILING / 2 + 3

        self.blocks = blocks(BLOCK_COUNT, BLOCK_DIST, BLOCK_WIDTH,
                             HOLE, self.y_max, self.x_max, self.startpoint)

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
        block_coordinates = self.blocks.nearest_block_coordinates(
            self.birds[0].x)

        for bird in self.birds:

            if not bird.dead:
                bird.update(self.get_size()[0])

            # Check for collision
            # Multiply with a factor so it feels better
            if self.blocks.check_collision(bird.x, bird.y, bird.width, bird.height):
                bird.die()

            # Check if a bird passed a pipe
            if bird.nearest_block != block_coordinates[8] and not bird.dead:
                bird.add_score()
                # print("Got through one!")
                bird.nearest_block = block_coordinates[8]

            # Check if all birds are dead. If one bird is alive the game is not stopped
            if not bird.dead:
                stop_game = False

        # If all birds are dead the game is get restarted and if no bird passed a single pipe a new population of birds is created
        if stop_game:
            # Check the score
            check = self.check_best_bird()
            best_birds = check[1]
            score = check[0]

            print("The score of the best bird was: " +
                 str(score))
            print("The best bird was number: " + str(best_birds))

            # If the score is 0, create a new population
            if best_birds is None:
                print("No one made it :(")
                self.birds = [flappy_bird(x=50, y=self.y_max/2, gravity=GRAVITY,
                                          jump_height=JUMP_HIGHT, radius=BIRDSIZE) for i in range(BIRD_COUNT)]
            else:
                print("Birds are learning...")
                # If more than one bird made it as far as he got split the next generation up and let them learn from the different birds.
                steps = len(best_birds)
                for num, best_bird in enumerate(best_birds):
                    lower_boundaries = round((num/steps) * len(self.birds))
                    upper_boundaries = round(((num+1)/steps) * len(self.birds))
                    for num, bird in enumerate(self.birds[lower_boundaries:upper_boundaries]):
                        if num not in best_birds:
                            bird.learn_from_other_bird(self.birds[best_bird])
                            # bird.change_color((0, 255 * upper_boundaries, 255 * upper_boundaries))
                        else:
                            pass
                            # bird.change_color((0, 0,255 * upper_boundaries))

            # Restart the game
            self.restart()

        score = self.check_best_bird()
        if score is not None:
            self.max_score = score[0]
        self.score_text.text = "Score : " + str(self.max_score)

    def bird_decisions(self, timer):
        """
        A explicit function to let the birds decide an and don't do that in every step of the update.

        Args:
            self (undefined):
            timer (undefined):

        """

        x_max = self.get_size()[1]
        y_max = self.get_size()[0]

        # [x_bot_left, y_bot_left, x_bot_right, y_top_right, x_top_right, y_top_right, x_top_left, y_top_left, block_number]
        block_coordinates = self.blocks.nearest_block_coordinates(
            self.birds[0].x)
        self.blocks.change_color(block_coordinates[8])

        for bird in self.birds:
            if not bird.dead:
                # Calculate the distances to the nearest pipe
                y_top = (bird.y - block_coordinates[7]) / 2 * y_max + 1
                y_bot = (bird.y - block_coordinates[1]) / 2 * y_max + 1
                dist_block = abs(bird.x - block_coordinates[2]) / x_max
                # y_bird = bird.y / y_max
                velocity_bird = (bird.velocity / 20) + 1

                # Ask the bird what he wants to do
                bird.decide_NN([y_top, y_bot, dist_block, velocity_bird])

    def check_best_bird(self) -> int:
        """
        Check for the best bird.

        Args:
            self (undefined):

        Returns:
            list: The score and the list positions of the best birds or None if all birds failed.

        """

        max_score = 0
        best_birds = []

        for bird in self.birds:
            if bird.score > max_score:
                max_score = bird.score

        for num, bird in enumerate(self.birds):
            if bird.score == max_score:
                best_birds.append(num)

        if max_score == 0:
            return None
        
        return [max_score, best_birds]

    def on_draw(self):
        """
        Draw all the objects in the app:
        - The blocks
        - The bird / birds

        Args:
            self (undefined):

        """
        self.clear()

        self.background.draw()

        self.blocks.draw()

        for bird in self.birds:
            if not bird.dead:
                bird.draw()

        # [x_bot_left, y_bot_left, x_bot_right, y_top_right, x_top_right, y_top_right, x_top_left, y_top_left, block_number]
        block_coordinates = self.blocks.nearest_block_coordinates(
            self.birds[0].x)

        # Draw the edges of the nearest Block
        pyglet.shapes.Circle(x=block_coordinates[0], y=block_coordinates[1],
                             radius=5, color=(100, 0, 0)).draw()
        pyglet.shapes.Circle(x=block_coordinates[2], y=block_coordinates[3],
                             radius=5, color=(100, 0, 0)).draw()

        pyglet.shapes.Circle(x=block_coordinates[4],
                             y=block_coordinates[5], radius=5, color=(100, 0, 0)).draw()
        pyglet.shapes.Circle(x=block_coordinates[6], y=block_coordinates[7],
                             radius=5, color=(100, 0, 0)).draw()

        self.score_text.draw()

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
                             HOLE, self.y_max, self.x_max, self.startpoint)

        self.started = False
        self.max_score = 0

        # Revive all birds
        for bird in self.birds:
            bird.revive(JUMP_HIGHT, self.y_max/2)

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
                pyglet.clock.schedule_interval(
                    self.bird_decisions, NN_DECISION_SPEED)
                self.started = True
            # self.birds[1].move_up()
        if symbol == pyglet.window.key.ESCAPE:
            self.close()
