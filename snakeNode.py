from dataclasses import dataclass
from typing import Optional
from typing_extensions import Self
from customExceptions import BrokenGameLogicException
from positionHolder import _PositionHolder
from direction import Direction


@dataclass
class SnakeNode(_PositionHolder):
  nextnode: Optional[Self] = None

  def getShiftedNode(self, direction: Direction, nextnode: Optional[Self] = None) -> Self:
    return SnakeNode(
      self.position.getNewPositionBy(direction),
      nextnode,
    )

  @property
  def selfToNextNodeDirection(self):
    return self.__calcDirection(
      Direction.bottom,
      Direction.top,
      Direction.left,
      Direction.right,
    )

  @property
  def nextNodeToSelfDirection(self):
    return self.__calcDirection(
      Direction.top,
      Direction.bottom,
      Direction.right,
      Direction.left,
    )

  def __calcDirection(self,
    whenSelfYBigger: Direction,
    whenSelfYSmaller: Direction,
    whenSelfXBigger: Direction,
    whenSelfXLower: Direction
  ) -> Direction:
    if self.nextnode is None:
      raise BrokenGameLogicException('Cannot get directionOfNextNode for node without next node')

    match [self.position.x - self.nextnode.position.x, self.position.y - self.nextnode.position.y]:
      case [0, 1]:
        return whenSelfYBigger
      case [0, -1]:
        return whenSelfYSmaller
      case [1, 0]:
        return whenSelfXBigger
      case [-1, 0]:
        return whenSelfXLower
      case _:
        raise BrokenGameLogicException(f'Impossible situation when nextnode.position={self.nextnode.position} and self.position={self.position} are not left-right-top-bottom neighbours')
