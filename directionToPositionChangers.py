from typing import Callable, Tuple

from direction import Direction


PositionChanger = Callable[[int], int]
PositionChangerForX = PositionChanger
PositionChangerForY = PositionChanger
PositionChangerPair = Tuple[PositionChangerForX, PositionChangerForY]

directionToPositionChangers: dict[Direction, PositionChangerPair] = {
  Direction.top:    (lambda x: x,     lambda y: y + 1),
  Direction.bottom: (lambda x: x,     lambda y: y - 1),
  Direction.right:  (lambda x: x + 1, lambda y: y    ),
  Direction.left:   (lambda x: x - 1, lambda y: y    ),
}
