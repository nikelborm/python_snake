from enum import Enum


class Direction(Enum):
  TOP = 1
  BOTTOM = 2
  RIGHT = 3
  LEFT = 4

HORIZONTAL_DIRECTIONS = {Direction.RIGHT, Direction.LEFT}
VERTICAL_DIRECTIONS = {Direction.BOTTOM, Direction.TOP}
