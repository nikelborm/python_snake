from dataclasses import dataclass
from typing import Optional
from customExceptions import BrokenGameLogicException
from positionHolder import _PositionHolder
from direction import Direction


@dataclass
class SnakeNode(_PositionHolder):
    nextNode: Optional['SnakeNode'] = None

    def getNewNodeShiftedInto(
        self,
        direction: Direction,
        nextNode: Optional['SnakeNode'] = None
    ) -> 'SnakeNode':
        return SnakeNode(
            self.position.getNewPositionShiftedInto(direction),
            nextNode,
        )

    @property
    def selfToNextNodeDirection(self):
        return self.__calcDirection(
            Direction.BOTTOM,
            Direction.TOP,
            Direction.LEFT,
            Direction.RIGHT,
        )

    @property
    def nextNodeToSelfDirection(self):
        return self.__calcDirection(
            Direction.TOP,
            Direction.BOTTOM,
            Direction.RIGHT,
            Direction.LEFT,
        )

    def __calcDirection(
        self,
        whenSelfYBigger: Direction,
        whenSelfYSmaller: Direction,
        whenSelfXBigger: Direction,
        whenSelfXLower: Direction
    ) -> Direction:
        if self.nextNode is None:
            raise BrokenGameLogicException(
                'Cannot get directionOfNextNode for node without next node'
            )

        match [
            self.position.x - self.nextNode.position.x,
            self.position.y - self.nextNode.position.y
        ]:
            case [0, 1]:
                return whenSelfYBigger
            case [0, -1]:
                return whenSelfYSmaller
            case [1, 0]:
                return whenSelfXBigger
            case [-1, 0]:
                return whenSelfXLower
            case _:
                raise BrokenGameLogicException(
                    f'''Impossible situation when nextNode.position={
                        self.nextNode.position
                    } and self.position={
                        self.position
                    } are not left-right-top-bottom neighbours'''
                )
