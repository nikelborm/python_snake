from dataclasses import dataclass
import sys
from typing import Callable, Dict, List, Literal, Optional, Tuple, TypedDict, Union
from typing_extensions import Self
import pygame





# Difficulty settings
# Easy      ->  10
# Medium    ->  25
# Hard      ->  40
# Harder    ->  60
# Impossible->  120
DIFFICULTY = 25

# Window size
FRAME_SIZE_X = 720
FRAME_SIZE_Y = 480






PositionChanger = Callable[[int], int]
PositionChangerForX = PositionChanger
PositionChangerForY = PositionChanger
PositionChangerPair = Tuple[PositionChangerForX, PositionChangerForY]

class DirectionToPositionChangers(TypedDict):
  above:        PositionChangerPair
  under:        PositionChangerPair
  to_the_right: PositionChangerPair
  to_the_left:  PositionChangerPair

# 2  *  *  *
#
# 1  *  *  *
#
# 0  *  *  *
# ^
# y
# x->0  1  2

directionToPositionChangers: DirectionToPositionChangers = {
  'above':        (lambda x: x,     lambda y: y + 1),
  'under':        (lambda x: x,     lambda y: y - 1),
  'to_the_right': (lambda x: x + 1, lambda y: y    ),
  'to_the_left':  (lambda x: x - 1, lambda y: y    ),
}


PossibleDirection = Literal['above', 'under', 'to_the_right', 'to_the_left']


@dataclass
class Position:
  x: int
  y: int

  def getNewPositionBy(self, direction: PossibleDirection) -> 'Position':
    changeX, changeY = directionToPositionChangers[direction]

    return Position(
      x=changeX(self.x),
      y=changeY(self.y)
    )


@dataclass
class _PositionHolder():
  position: Position

@dataclass
class Candy(_PositionHolder):
  colour: Literal['blue, yellow', 'red']
  size: int


@dataclass
class Node(_PositionHolder):
  nextnode: Optional[Self] = None

  def getShiftedNode(self, direction: PossibleDirection, nextnode: Optional[Self] = None) -> Self:
    return Node(
      self.position.getNewPositionBy(direction),
      nextnode,
    )


class GameOverException(Exception):
  pass


class PositionToHolderMap:
  def __init__(self):
    self.__store: Dict[str, _PositionHolder] = {}

  def add(self, holder: _PositionHolder):
    self.__store[self.__getHashOf(holder.position)] = holder

  def getBy(self, position: Position) -> Optional[_PositionHolder]:
    return self.__store.get(self.__getHashOf(position))

  def remove(self, holder: _PositionHolder):
    self.removeBy(holder.position)

  def removeBy(self, position: Position):
    del self.__store[self.__getHashOf(position)]

  def getAll(self):
    return self.__store.values()

  def __getHashOf(self, position: Position):
    return f'{position.x}_{position.y}'





class Snake:
  def __init__(self):
    self.__cachedNodeMap = PositionToHolderMap()
    self.__headNode = Node(Position(0, 1))
    self.__tailNode = Node(Position(0, 0), self.__headNode)
    self.__cachedNodeMap.add(self.__headNode)
    self.__cachedNodeMap.add(self.__tailNode)

  def makeStep(self, direction: PossibleDirection, shouldBodyGrow: bool):
    self.__stepByHead(direction)
    if not shouldBodyGrow:
      self.__stepByTail()

  def isHeadMovePossibleTo(self, direction: PossibleDirection) -> bool:
    return self.__cachedNodeMap.getBy(
      self.__headNode.position.getNewPositionBy(direction)
    ) is None

  def __stepByTail(self):
    oldTailNode = self.__tailNode
    self.__tailNode = oldTailNode.nextnode
    self.__cachedNodeMap.remove(oldTailNode)
    del oldTailNode

  def __stepByHead(self, direction: PossibleDirection):
    self.__headNode = self.__headNode.nextnode = self.__headNode.getShiftedNode(direction)
    self.__cachedNodeMap.add(self.__headNode)

  @property
  def headPosition(self):
    return Position(self.__headNode.position.x, self.__headNode.position.y)



class CandyMap:
  def __init__(self):
    self.__cachedCandyMap = PositionToHolderMap()

  def reduceAllCandiesSizeByOne(self):
    for candy in self.getAllCandies():
      candy.size = candy.size

      if candy.size == 0:
        self.__cachedCandyMap.remove(candy)

  def getCandyBy(self, position: Position) -> Optional[Candy]:
    return self.__cachedCandyMap.getBy(position)  # type: ignore

  def removeCandyBy(self, position: Position):
    return self.__cachedCandyMap.removeBy(position)

  def getAllCandies(self) -> List[Candy]:
    return list(self.__cachedCandyMap.getAll())  # type: ignore




class GameEngine:
  __snake = Snake()
  __candiesField = CandyMap()

  def makeGameIteration(self, direction: PossibleDirection):
    if not self.__snake.isHeadMovePossibleTo(direction):
      raise GameOverException('Head tried to eat body of the snake')

    doesHeadFacesCandy = self.__doesHeadFacesCandy(direction)

    self.__snake.makeStep(direction, doesHeadFacesCandy)

    if doesHeadFacesCandy:
      self.__candiesField.removeCandyBy(self.__snake.headPosition)

    self.__candiesField.reduceAllCandiesSizeByOne()

  def __doesHeadFacesCandy(self, direction: PossibleDirection) -> bool:
    return self.__candiesField.getCandyBy(
      self.__snake.headPosition.getNewPositionBy(direction)
    ) is None





if __name__ == 'main':
  check_errors = pygame.init()
  # pygame.init() example output -> (6, 0)
  # second number in tuple gives number of errors
  if check_errors[1] > 0:
      print(f'[!] Had {check_errors[1]} errors when initialising game, exiting...')
      sys.exit(-1)
  else:
      print('[+] Game successfully initialised')

  pygame.display.set_caption('Snake Eater')
  game_window = pygame.display.set_mode((frame_size_x, frame_size_y))
  game = GameEngine()
  game.makeGameIteration('above')
  game.makeGameIteration('above')
  game.makeGameIteration('to_the_right')
  game.makeGameIteration('to_the_right')
  game.makeGameIteration('under')
