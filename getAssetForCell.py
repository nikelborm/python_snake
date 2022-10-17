from gameCellKind import GameCellKind
import pygame
from constant import GAME_FIELD_BACKGROUND_COLOR, SNAKE_BODY_COLOR


def getAssetForCell(cellKind: GameCellKind):
    pass


def getColorForCell(cellKind: GameCellKind):
    return cellKindToCellColorMap[cellKind]


cellKindToCellColorMap: dict[GameCellKind, pygame.Color] = {
    GameCellKind.HEAD_TO_BOTTOM: SNAKE_BODY_COLOR,
    GameCellKind.HEAD_TO_TOP: SNAKE_BODY_COLOR,
    GameCellKind.HEAD_TO_LEFT: SNAKE_BODY_COLOR,
    GameCellKind.HEAD_TO_RIGHT: SNAKE_BODY_COLOR,

    GameCellKind.TAIL_TO_BOTTOM: SNAKE_BODY_COLOR,
    GameCellKind.TAIL_TO_TOP: SNAKE_BODY_COLOR,
    GameCellKind.TAIL_TO_LEFT: SNAKE_BODY_COLOR,
    GameCellKind.TAIL_TO_RIGHT: SNAKE_BODY_COLOR,

    GameCellKind.HORIZONTAL_BODY: SNAKE_BODY_COLOR,
    GameCellKind.VERTICAL_BODY: SNAKE_BODY_COLOR,
    GameCellKind.VOID: GAME_FIELD_BACKGROUND_COLOR,
}
