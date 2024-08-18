import pygame, sys
import random

# Setup
WIDTH, HEIGHT = 1400, 720
win = pygame.display.set_mode((WIDTH, HEIGHT))

# Colors
random_red = random.randint(0, 255)
random_blue = random.randint(0, 255)
random_green = random.randint(0, 255)
RAINBOW = ((random_red), (random_blue), (random_green))
LIGHT_BLUE = (150, 150, 200)
BLACK = (0, 0, 0)
DARK_BLUE = (100, 0, 200)
COLOR_DARK = (50, 50, 50)
COLOR_LIGHT = (100, 100, 100)
COLOR = (255, 255, 255)
GOLD = ("gold")
WHITE = ('white')

# Riddle Me
# Constants
FONT_SIZE = 36
TEXT_COLOR = (0, 0, 0)
BUTTON_COLOR = (0, 128, 0)
BUTTON_HOVER_COLOR = (0, 255, 0)
INPUT_BOX_COLOR = (200, 200, 200)
BUTTON_FONT_SIZE = 48