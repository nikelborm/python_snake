import pygame
from direction import Direction
from position import Position


# Difficulty settings
# Easy       ->    10
# Medium     ->    25
# Hard       ->    40
# Harder     ->    60
# Impossible ->    120
DIFFICULTY = 1

# CELL_RENDERER = 'color'
CELL_RENDERER = 'asset'

GAME_GRID_X_SIZE_IN_GAME_CELLS = 16 * 2
GAME_GRID_Y_SIZE_IN_GAME_CELLS = 9 * 2

CELL_SIZE_IN_PIXELS = 60

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
