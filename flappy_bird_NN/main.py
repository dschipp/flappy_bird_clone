import os, sys
path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(path)
__docformat__ = "google"

import pyglet
from window import app
import logging
from logging import config
import constants
import json

with open(path + "/../data/log_config.json", 'rt') as conf_file:
    conf = json.load(conf_file)
config.dictConfig(conf)
conf_file.close()

if __name__ == '__main__':
    logging.info("Start app with update speed: " + str(constants.GAME_SPEED))

    window = app()
    pyglet.app.run()
