import pygame
from direction import Direction
from position import Position

# At the moment difficulty doesn't depend only on this number, because
# speed will feel different on different grid sizes

# Speed settings (FPS basically)
# Easy       ->    10
# Medium     ->    15
# Hard       ->    20
# Quite hard ->    25
# Very hard  ->    30
# Insane     ->    60 - use it only if you have 40 years old PC
# Impossible ->    120
SPEED = 5 # 5 feels quite nice and playable at 16 * 16 grid

# CELL_RENDERER = 'color'
CELL_RENDERER = 'asset'

GAME_GRID_X_SIZE_IN_GAME_CELLS = 16
GAME_GRID_Y_SIZE_IN_GAME_CELLS = 16

CELL_SIZE_IN_PIXELS = 80

WINDOW_SIZE_X = GAME_GRID_X_SIZE_IN_GAME_CELLS * CELL_SIZE_IN_PIXELS
WINDOW_SIZE_Y = GAME_GRID_Y_SIZE_IN_GAME_CELLS * CELL_SIZE_IN_PIXELS


BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
RED = pygame.Color(255, 0, 0)
GREEN = pygame.Color(0, 255, 0)
BLUE = pygame.Color(0, 0, 255)
YELLOW = pygame.Color(253, 216, 53)


GAME_FIELD_BACKGROUND_COLOR = BLACK
SNAKE_BODY_COLOR = GREEN
GAME_OVER_TEXT_COLOR = RED
GAME_OVER_BACKGROUND_COLOR = BLACK

# usefull for debugging
PREDEFINED_STEPS = [
  Direction.TOP,
  Direction.TOP,
  Direction.TOP,
  Direction.TOP,
  Direction.TOP,
  Direction.TOP,
  Direction.TOP,
  Direction.RIGHT,
  Direction.RIGHT,
  Direction.RIGHT,
  Direction.RIGHT,
  Direction.RIGHT,
  Direction.BOTTOM,
  Direction.BOTTOM,
  Direction.BOTTOM,
  Direction.BOTTOM,
  Direction.BOTTOM,
  Direction.LEFT,
  Direction.LEFT,
  Direction.LEFT,
  Direction.LEFT,
  Direction.TOP,
  Direction.RIGHT,
  Direction.RIGHT,
  Direction.BOTTOM,
  Direction.RIGHT,
  Direction.RIGHT,
  Direction.RIGHT,
  Direction.RIGHT
]

changeablePredefinedSteps = [*PREDEFINED_STEPS]

USE_PREDEFINED_STEPS = False


ALL_POSSIBLE_POSITIONS = {
  Position(x, y)
  for x in range(GAME_GRID_X_SIZE_IN_GAME_CELLS)
  for y in range(GAME_GRID_Y_SIZE_IN_GAME_CELLS)
}
