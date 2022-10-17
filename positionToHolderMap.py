from typing import Dict, Optional
from position import Position
from positionHolder import _PositionHolder


class PositionToHolderMap:
    def __init__(self):
        self.store: Dict[int, _PositionHolder] = {}

    def add(self, *holders: _PositionHolder):
        for holder in holders:
            self.store[hash(holder.position)] = holder

    def getBy(self, position: Position) -> Optional[_PositionHolder]:
        return self.store.get(hash(position))

    def remove(self, holder: _PositionHolder):
        self.removeBy(holder.position)

    def removeBy(self, position: Position):
        del self.store[hash(position)]

    def getAll(self):
        return list(self.store.values())
