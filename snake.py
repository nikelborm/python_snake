from typing import List
from customExceptions import BrokenGameLogicException
from gameCellKind import GameCellKind
from neckDirection import ComplexNeckDirection
from position import Position
from snakeNode import SnakeNode
from positionToHolderMap import PositionToHolderMap
from direction import Direction


class Snake:
    def __init__(self):
        self.__cachedNodeMap = PositionToHolderMap()
        self.__headNode = SnakeNode(Position(0, 2))
        self.__neckNode = SnakeNode(Position(0, 1), self.__headNode)
        self.__tailNode = SnakeNode(Position(0, 0), self.__neckNode)
        self.__nodeBeforeNeck = self.__tailNode
        self.__cachedNodeMap.add(
            self.__tailNode,
            self.__neckNode,
            self.__headNode
        )

    @property
    def headPosition(self):
        return Position(self.__headNode.position.x, self.__headNode.position.y)

    @property
    def headDirection(self):
        return self.__neckNode.selfToNextNodeDirection

    @property
    def tailDirection(self):
        return self.__tailNode.nextNodeToSelfDirection

    def makeStepAndGetPositionsChangedTheirLook(
        self,
        direction: Direction,
        shouldBodyGrow: bool
    ) -> List[Position]:  # sourcery skip: remove-pass-body
        cellsPositionsChangedTheirLook: List[Position] = []
        positionOfFutureHead = self.headPosition.getNewPositionShiftedInto(
            direction
        )

        if shouldBodyGrow:
            # in case when candy in front of snake's face we leave tail on its
            # position and skip rerendering of tail.
            # we also guarantee that candy cannot be placed on tail's position.
            pass
        else:
            if positionOfFutureHead != self.__tailNode.position:
                cellsPositionsChangedTheirLook.append(self.__tailNode.position)
            self.__stepByTail()
            cellsPositionsChangedTheirLook.append(self.__tailNode.position)

        self.__stepByHead(direction)

        cellsPositionsChangedTheirLook.extend([
            self.__neckNode.position,
            self.headPosition
        ])

        return cellsPositionsChangedTheirLook

    def willSnakeBiteItselfAfterMove(self, direction: Direction) -> bool:
        newHeadPosition = self.__headNode.position.getNewPositionShiftedInto(
            direction
        )
        return (
            self.__cachedNodeMap.getBy(newHeadPosition) is not None
            and newHeadPosition != self.__tailNode.position
        )

    def getGameCellKindBy(self, position: Position) -> GameCellKind | None:
        # it intentionally made to be able to render only neck, tail and head,
        # because only those cells will actually change their view
        # if you want to render every snake's node at any moment you have
        # to add snakenode.previousNode link and it is actually a lot of work
        snakeNode = self.__cachedNodeMap.getBy(position)

        if snakeNode is None:
            return None

        if position == self.__headNode.position:
            return GameCellKind[f'HEAD_TO_{self.headDirection.name}']

        if position == self.__tailNode.position:
            return GameCellKind[f'TAIL_TO_{self.tailDirection.name}']

        if position == self.__neckNode.position:
            complexNeckDirection = self.__neckDirection
            return GameCellKind[
                f'''SNAKE_{
                    complexNeckDirection.incomingFrom.name
                }_TO_{
                    complexNeckDirection.outcomingTo.name
                }_CORNER'''
            ]

        raise BrokenGameLogicException(
            f'''You tried to get the game cell kind by the position={
                position
            } which happened to be not neck, tail, or head'''
        )

    @property
    def __neckDirection(self):
        return ComplexNeckDirection(
            self.__nodeBeforeNeck.selfToNextNodeDirection,
            self.__neckNode.selfToNextNodeDirection
        )

    def __stepByTail(self):
        tailNodeToRemove = self.__tailNode
        nodeToBecomeTail: SnakeNode = tailNodeToRemove.nextNode  # type: ignore
        self.__tailNode = nodeToBecomeTail
        tailNodeToRemove.nextNode = None
        self.__cachedNodeMap.remove(tailNodeToRemove)
        del tailNodeToRemove

    def __stepByHead(self, direction: Direction):
        self.__nodeBeforeNeck = self.__neckNode
        self.__neckNode = self.__headNode
        self.__headNode = self.__headNode.getNewNodeShiftedInto(direction)
        self.__neckNode.nextNode = self.__headNode
        self.__cachedNodeMap.add(self.__headNode)
