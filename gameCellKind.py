from enum import Enum


class GameCellKind(Enum):
    HEAD_TO_LEFT = 1
    HEAD_TO_RIGHT = 2
    HEAD_TO_TOP = 3
    HEAD_TO_BOTTOM = 4
    TAIL_TO_LEFT = 5
    TAIL_TO_RIGHT = 6
    TAIL_TO_TOP = 7
    TAIL_TO_BOTTOM = 8
    VOID = 9
    RED_CANDY = 10
    BLUE_CANDY = 11
    YELLOW_CANDY = 12
    HORIZONTAL_BODY = 13
    VERTICAL_BODY = 13
