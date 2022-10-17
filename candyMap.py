from typing import List, Optional
from candyColor import CandyColor
from gameCellKind import GameCellKind
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

    def createNewCandy(
        self,
        position: Position,
        color: CandyColor,
        size: int
    ):
        candy = Candy(position, color, size)
        self.__cachedCandyMap.add(candy)
        return candy

    def getCandyBy(self, position: Position) -> Optional[Candy]:
        return self.__cachedCandyMap.getBy(position)  # type: ignore

    def removeCandyBy(self, position: Position):
        return self.__cachedCandyMap.removeBy(position)

    def getAllCandies(self) -> List[Candy]:
        return self.__cachedCandyMap.getAll()  # type: ignore

    def getGameCellKindBy(self, position: Position) -> GameCellKind | None:
        candy = self.getCandyBy(position)

        return None if candy is None \
            else GameCellKind[f'{candy.color.name}_CANDY']
