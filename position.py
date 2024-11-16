from dataclasses import dataclass
from direction import Direction
from directionToPositionChangers import directionToPositionChangers


@dataclass(order=True, unsafe_hash=True)
class Position:
    x: int
    y: int

    def getNewPositionShiftedInto(self, direction: Direction) -> 'Position':
        changeX, changeY = directionToPositionChangers[direction]

        return Position(
            x=changeX(self.x),
            y=changeY(self.y)
        )
