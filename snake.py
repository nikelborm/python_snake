from typing import Optional
from position import Position
from snakeNode import SnakeNode
from positionToHolderMap import PositionToHolderMap
from direction import HORIZONTAL_DIRECTIONS, VERTICAL_DIRECTIONS, Direction


class Snake:
  def __init__(self):
    self.__cachedNodeMap = PositionToHolderMap()
    self.__headNode = SnakeNode(Position(0, 1))
    self.__tailNode = SnakeNode(Position(0, 0), self.__headNode)
    self.__neckNode = self.__tailNode
    self.__cachedNodeMap.add(self.__headNode)
    self.__cachedNodeMap.add(self.__tailNode)

  @property
  def headPosition(self):
    return Position(self.__headNode.position.x, self.__headNode.position.y)

  @property
  def headDirection(self):
    return self.__neckNode.selfToNextNodeDirection

  @property
  def tailPosition(self):
    return Position(self.__tailNode.position.x, self.__tailNode.position.y)

  @property
  def tailDirection(self):
    return self.__tailNode.nextNodeToSelfDirection

  def makeStep(self, direction: Direction, shouldBodyGrow: bool):
    self.__stepByHead(direction)
    if not shouldBodyGrow:
      self.__stepByTail()

  def isHeadMovePossibleTo(self, direction: Direction) -> bool:
    newHeadPosition = self.__headNode.position.getNewPositionBy(direction)
    return self.__cachedNodeMap.getBy(newHeadPosition) is None \
      or newHeadPosition == self.tailPosition

  def getNextHeadDirection(self, directionFromKeyboard: Optional[Direction]) -> Direction:
    if (self.headDirection in HORIZONTAL_DIRECTIONS and directionFromKeyboard in HORIZONTAL_DIRECTIONS) \
    or (self.headDirection in VERTICAL_DIRECTIONS and directionFromKeyboard in VERTICAL_DIRECTIONS) \
    or directionFromKeyboard is None:
      return self.headDirection

    return directionFromKeyboard



  def __stepByTail(self):
    tailNodeToDissapear = self.__tailNode
    nodeToBecomeTail: SnakeNode = tailNodeToDissapear.nextnode  # type: ignore
    self.__tailNode = nodeToBecomeTail
    tailNodeToDissapear.nextnode = None
    self.__cachedNodeMap.remove(tailNodeToDissapear)
    del tailNodeToDissapear

  def __stepByHead(self, direction: Direction):
    newHeadNode = self.__headNode.getShiftedNode(direction)
    self.__neckNode = self.__headNode
    self.__headNode = newHeadNode
    self.__neckNode.nextnode = self.__headNode
    self.__cachedNodeMap.add(self.__headNode)
