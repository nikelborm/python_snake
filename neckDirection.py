from dataclasses import dataclass

from direction import Direction


@dataclass
class ComplexNeckDirection():
    incomingFrom: Direction
    outcomingTo: Direction
