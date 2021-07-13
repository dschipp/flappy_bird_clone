"""
A class for the main menu displayed when the game is started or stopped.
Shows game instructions and has a option menu for to change the properties of the game.
"""
# TODO: In the Background show a blurred version of the game played by a very good and saved bird

import pyglet

class menu:
    def __init__(self, x_middle, y_middle) -> None:
        
        self.x_middle = x_middle
        self.y_middle = y_middle

        self.start_game_instructions_text = pyglet.text.Label('To Start the game press Space or Arrow Up',
                                            font_name='Times New Roman',
                                            font_size=15, color=(0, 0, 0, 255),
                                            x=self.x_middle- 150, y=self.y_middle + 15)
        
        self.save_load_instructions_text = pyglet.text.Label('To save the best bird press S or to load the saved best bird press L',
                                            font_name='Times New Roman',
                                            font_size=15, color=(0, 0, 0, 255),
                                            x=self.x_middle - 150, y=self.y_middle - 15)
        

    def draw(self):
        
        self.start_game_instructions_text.draw()
        self.save_load_instructions_text.draw()



"""
To display a Message or information that maybe is displayed in the terminal.
"""
class error_messages:
    def __init__(self) -> None:
        pass

    def draw(self):
        pass
    