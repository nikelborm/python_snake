from typing import List, Optional
from positionToHolderMap import PositionToHolderMap
from position import Position
from candy import Candy


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
