import os, sys
path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(path)
__docformat__ = "google"

import pyglet
from window import app
import logging
from logging import config

log_config = {
    "version":1,
    "root":{
        "handlers" : ["log_handler"],
        "level": "DEBUG"
    },
    "handlers":{
        "log_handler":{
            "formatter": "std_out",
            "class": "logging.FileHandler",
            "level": "DEBUG",
            "filename":"app.log"
        }
    },
    "formatters":{
        "std_out": {
            "format": "%(asctime)s : %(levelname)s : %(module)s : %(funcName)s : %(lineno)d : %(message)s",
            "datefmt":"%d-%m-%Y %I:%M:%S"
        }
    },
}

config.dictConfig(log_config)

if __name__ == '__main__':
    logging.info("Start app")

    window = app()
    pyglet.app.run()
