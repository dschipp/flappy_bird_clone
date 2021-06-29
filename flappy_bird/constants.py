""" The Game configs are read from the config.ini file """

import configparser

config = configparser.ConfigParser()
config.read("./data/config.ini")

""" ---------------- Game Properties ----------------------- """
GAME_SPEED = float(config['Game']['GAME_SPEED'])  # How often is the update function of the game called.
DISPLAYED_BIRDS = int(config['Game']['DISPLAYED_BIRDS'])  # How Many Birds are displayed on the window.

""" ---------------- Bird Properties ----------------------- """
JUMP_HEIGHT = int(config['Bird']['JUMP_HEIGHT'])  # How strong do the birds jump.
GRAVITY = float(config['Bird']['GRAVITY'])  # # How strong are the birds pulled down.
BIRD_SIZE = int(config['Bird']['BIRD_SIZE'])  # The Size of the Bird.
BIRD_X = int(config['Bird']['BIRD_SIZE']) # The x coordinate of the Birds.

""" ------------- Neuronal Network Properties -------------- """
NN_DECISION_SPEED = float(config['NeuralNet']['NN_DECISION_SPEED'])  # How often are the Neural Network functions called.
BIRD_COUNT = int(config['NeuralNet']['BIRD_COUNT'])  # Of how many birds does one Population consists.

""" ---------------- Block Properties ---------------------- """
BLOCK_MAX_HEIGHT = int(config['Block']['BLOCK_MAX_HEIGHT'])
BLOCK_MIN_HEIGHT = int(config['Block']['BLOCK_MIN_HEIGHT'])
BLOCK_WIDTH = int(config['Block']['BLOCK_WIDTH'])
BLOCK_SPEED = int(config['Block']['BLOCK_SPEED'])
BLOCK_SPEEDUP = float(config['Block']['BLOCK_SPEEDUP'])
BLOCK_HOLE = int(config['Block']['BLOCK_HOLE'])
BLOCK_COUNT = int(config['Block']['BLOCK_COUNT'])
BLOCK_DIST = int(config['Block']['BLOCK_DIST'])
BLOCK_STARTPOINT = int(config['Block']['BLOCK_STARTPOINT'])
