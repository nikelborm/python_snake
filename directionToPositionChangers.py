from typing import Callable, Tuple
from direction import Direction


PositionChanger = Callable[[int], int]
PositionChangerForX = PositionChanger
PositionChangerForY = PositionChanger
PositionChangerPair = Tuple[PositionChangerForX, PositionChangerForY]

directionToPositionChangers: dict[Direction, PositionChangerPair] = {
    Direction.TOP:    (lambda x: x,     lambda y: y + 1),
    Direction.BOTTOM: (lambda x: x,     lambda y: y - 1),
    Direction.RIGHT:  (lambda x: x + 1, lambda y: y    ),
    Direction.LEFT:   (lambda x: x - 1, lambda y: y    ),
}
