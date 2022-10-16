from enum import Enum


class GameCellKind(Enum):
  head_to_left = 1
  head_to_right = 2
  head_to_top = 3
  head_to_bottom = 4
  tail_to_left = 5
  tail_to_right = 6
  tail_to_top = 7
  tail_to_bottom = 8
  void = 9
  red_candy = 10
  blue_candy = 11
  yellow_candy = 12
