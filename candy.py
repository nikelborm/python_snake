from dataclasses import dataclass
from candyColour import CandyColour
from positionHolder import _PositionHolder


@dataclass
class Candy(_PositionHolder):
  colour: CandyColour
  size: int
