from gameCellKind import GameCellKind
import pygame
# from constant import BLUE, GAME_FIELD_BACKGROUND_COLOR
from constant import SNAKE_BODY_COLOR, RED, YELLOW, GAME_FIELD_BACKGROUND_COLOR, BLUE


def getAssetForCell(cellKind: GameCellKind):
    pass


def getColorForCell(cellKind: GameCellKind):
    return cellKindToCellColorMap[cellKind]


cellKindToCellColorMap: dict[GameCellKind, pygame.Color] = {
    GameCellKind.HEAD_TO_LEFT: SNAKE_BODY_COLOR,
    GameCellKind.HEAD_TO_RIGHT: SNAKE_BODY_COLOR,
    GameCellKind.HEAD_TO_TOP: SNAKE_BODY_COLOR,
    GameCellKind.HEAD_TO_BOTTOM: SNAKE_BODY_COLOR,

    GameCellKind.TAIL_TO_LEFT: SNAKE_BODY_COLOR,
    GameCellKind.TAIL_TO_RIGHT: SNAKE_BODY_COLOR,
    GameCellKind.TAIL_TO_TOP: SNAKE_BODY_COLOR,
    GameCellKind.TAIL_TO_BOTTOM: SNAKE_BODY_COLOR,

    GameCellKind.VOID: GAME_FIELD_BACKGROUND_COLOR,

    GameCellKind.RED_CANDY: RED,
    GameCellKind.BLUE_CANDY: BLUE,
    GameCellKind.YELLOW_CANDY: YELLOW,

    GameCellKind.HORIZONTAL_BODY: SNAKE_BODY_COLOR,

    GameCellKind.VERTICAL_BODY: SNAKE_BODY_COLOR,

    GameCellKind.SNAKE_TOP_TO_LEFT_CORNER: SNAKE_BODY_COLOR,
    GameCellKind.SNAKE_TOP_TO_RIGHT_CORNER: SNAKE_BODY_COLOR,
    GameCellKind.SNAKE_BOTTOM_TO_LEFT_CORNER: SNAKE_BODY_COLOR,
    GameCellKind.SNAKE_BOTTOM_TO_RIGHT_CORNER: SNAKE_BODY_COLOR,
}
