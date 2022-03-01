import os, sys
path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(path)
__docformat__ = "google"

import pyglet
from window import app

if __name__ == '__main__':
    window = app()
    pyglet.app.run()
