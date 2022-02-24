import os, sys
path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(path)

import pyglet
from window import app

if __name__ == '__main__':
    window = app()
    pyglet.app.run()
