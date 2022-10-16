from enum import Enum


class Direction(Enum):
  top = 1
  bottom = 2
  right = 3
  left = 4

HORIZONTAL_DIRECTIONS = {Direction.right, Direction.left}
VERTICAL_DIRECTIONS = {Direction.bottom, Direction.top}
