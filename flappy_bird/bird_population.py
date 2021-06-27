from bird import flappy_bird
import constants

class bird_population():
    def __init__(self, size : int) -> None:

        self.birds = [flappy_bird(x=50, y=self.y_max/2) for i in range(constants.BIRD_COUNT)]
