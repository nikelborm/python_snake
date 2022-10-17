import os
from gameCellKind import GameCellKind
from pygame import Color, surface, image, transform
from constant import CELL_SIZE_IN_PIXELS, SNAKE_BODY_COLOR, RED, YELLOW, \
    BLUE, GAME_FIELD_BACKGROUND_COLOR


def getAssetForCell(cellKind: GameCellKind):
    return cellKindToImageMap[cellKind]


def getColorForCell(cellKind: GameCellKind):
    return cellKindToCellColorMap[cellKind]


def loadImage(fileName: str) -> surface.Surface:
    imageAsset = image.load(os.path.join('assetsImages', f'{fileName}.png'))
    scaledImageAsset = transform.scale(
        imageAsset,
        (
            CELL_SIZE_IN_PIXELS,
            CELL_SIZE_IN_PIXELS
        )
    )
    scaledImageAsset.set_colorkey((0, 0, 0))
    return scaledImageAsset


cellKindToCellColorMap: dict[GameCellKind, Color] = {
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

cellKindToImageMap: dict[GameCellKind, surface.Surface] = {
    GameCellKind.HEAD_TO_LEFT: loadImage('leftHead'),
    GameCellKind.HEAD_TO_RIGHT: loadImage('rightHead'),
    GameCellKind.HEAD_TO_TOP: loadImage('upHead'),
    GameCellKind.HEAD_TO_BOTTOM: loadImage('downHead'),

    GameCellKind.TAIL_TO_LEFT: loadImage('leftTail'),
    GameCellKind.TAIL_TO_RIGHT: loadImage('rightTail'),
    GameCellKind.TAIL_TO_TOP: loadImage('upTail'),
    GameCellKind.TAIL_TO_BOTTOM: loadImage('downTail'),

    GameCellKind.VOID: loadImage('emptiness'),

    GameCellKind.RED_CANDY: loadImage('apple'),
    GameCellKind.BLUE_CANDY: loadImage('apple'),
    GameCellKind.YELLOW_CANDY: loadImage('apple'),

    GameCellKind.HORIZONTAL_BODY: loadImage('horizontalBody'),

    GameCellKind.VERTICAL_BODY: loadImage('verticalBody'),

    GameCellKind.SNAKE_TOP_TO_LEFT_CORNER: loadImage('leftUpBody'),
    GameCellKind.SNAKE_TOP_TO_RIGHT_CORNER: loadImage('rightUpBody'),
    GameCellKind.SNAKE_BOTTOM_TO_LEFT_CORNER: loadImage('leftDownBody'),
    GameCellKind.SNAKE_BOTTOM_TO_RIGHT_CORNER: loadImage('downRightBody'),
}
