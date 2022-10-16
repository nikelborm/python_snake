from typing import Dict, Optional
from position import Position
from positionHolder import _PositionHolder

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
