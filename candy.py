from dataclasses import dataclass
from candyColor import CandyColor
from positionHolder import _PositionHolder


@dataclass
class Candy(_PositionHolder):
  color: CandyColor
  size: int
