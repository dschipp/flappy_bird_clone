import os, sys
path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(path)

"""
A class for the main menu displayed when the game is started or stopped.
Shows game instructions and has a option menu for to change the properties of the game.
"""
# TODO: In the Background show a blurred version of the game played by a very good and saved bird

import pyglet


class menu:
    def __init__(self, x_middle, y_middle) -> None:
        """
        Draw the menu. Currently it is only text for the keyboard instructions.

        Args:
            self (undefined):
            x_middle (undefined): The x middle coordinate of the window.
            y_middle (undefined): The y middle coordinate of the window.

        Returns:
            None

        """

        self.x_middle = x_middle
        self.y_middle = y_middle

        self.start_game_instructions_text = pyglet.text.Label('- To Start the game press Space or Arrow Up',
                                                              font_name='Times New Roman',
                                                              font_size=15, color=(0, 0, 0, 255),
                                                              x=self.x_middle - 120, y=self.y_middle + 15)

        self.save_instructions_text = pyglet.text.Label('- To save the best bird press S',
                                                        font_name='Times New Roman',
                                                        font_size=15, color=(0, 0, 0, 255),
                                                        x=self.x_middle - 120, y=self.y_middle - 15)

        self.load_instructions_text = pyglet.text.Label('- To load the saved best bird press L',
                                                        font_name='Times New Roman',
                                                        font_size=15, color=(0, 0, 0, 255),
                                                        x=self.x_middle - 120, y=self.y_middle - 45)

        self.speed_up_instructions_text = pyglet.text.Label('- To speed up the game press the right arrow key',
                                                            font_name='Times New Roman',
                                                            font_size=15, color=(0, 0, 0, 255),
                                                            x=self.x_middle - 120, y=self.y_middle - 75)

        self.pause_instructions_text = pyglet.text.Label('- To Pause and resume the game press P',
                                                         font_name='Times New Roman',
                                                         font_size=15, color=(0, 0, 0, 255),
                                                         x=self.x_middle - 120, y=self.y_middle - 105)

    def draw(self):

        self.start_game_instructions_text.draw()
        self.save_instructions_text.draw()
        self.load_instructions_text.draw()
        self.speed_up_instructions_text.draw()
        self.pause_instructions_text.draw()


"""
To display a Message or information that maybe is displayed in the terminal.
"""


class error_messages:
    def __init__(self) -> None:
        pass

    def draw(self):
        pass
