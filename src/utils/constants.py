from pygame import Color
from utils.int_vect import Int_Vector

# Timing Info
MAX_FPS = 60
MS_IN_S = 1000

# Render Info
WIDTH = 70
HEIGHT = 30
PLAYER_SCREEN_BUFFER = 10

FONT_SIZE = 24
BLANK_CELL = " "
STAR_CELL = ""

# Colors
DEFAULT_BG_COLOR = Color(50, 50, 50)
DEFAULT_FG_COLOR = Color(255, 255, 255)

BLACK = Color(0, 0, 0)
WHITE = Color(255, 255, 255)
GRAY = Color(100, 100, 100)

# Input Info
KEY_REPEAT = 100

# Directions
UP = Int_Vector(0, -1)
DOWN = Int_Vector(0, 1)
LEFT = Int_Vector(-1, 0)
RIGHT = Int_Vector(1, 0)

ALL_DIRECTIONS = [UP, DOWN, LEFT, RIGHT]
