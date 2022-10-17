from typing import Optional
from candy import Candy
from candyColor import CandyColor
from customExceptions import BrokenGameLogicException, GameOverException
from direction import HORIZONTAL_DIRECTIONS, VERTICAL_DIRECTIONS, Direction
from gameCellKind import GameCellKind
from getAssetForCell import getAssetForCell, getColorForCell
from position import Position
from pyGameWindowController import PyGameWindowController
from snake import Snake
from candyMap import CandyMap
from constant import CELL_RENDERER, GAME_GRID_Y_SIZE_IN_GAME_CELLS, \
    GAME_GRID_X_SIZE_IN_GAME_CELLS


class GameEngine:
    def __init__(self):
        self.__windowController = PyGameWindowController()
        self.__setInitialGameState()

    def runGameLoop(self):
        while True:
            self.__makeGameIteration(
                self.__getNextHeadDirection(
                    self.__windowController.parsePyGameEvents()
                )
            )

            self.__windowController.updadeScreen()

    def __makeGameIteration(self, direction: Direction):
        if self.__snake.willSnakeBiteItselfAfterMove(direction):
            raise GameOverException('Head tried to eat body of the snake')

        if self.__willSnakeStepOutOfGameField(direction):
            raise GameOverException('Head tried to eat border of game field')

        candy: Candy = self.__candiesField.getCandyBy(
            self.__snake.headPosition.getNewPositionShiftedInto(direction)
        )  # type: ignore
        doesHeadFacesCandy = candy is not None

        cellsPositions = self.__snake.makeStepAndGetPositionsChangedTheirLook(
            direction,
            doesHeadFacesCandy
        )

        # every snake iteration we rerender only about 4 cells
        for position in cellsPositions:
            self.__renderCell(position)

        if doesHeadFacesCandy:
            self.__playerScore += candy.size
            self.__candiesField.removeCandyBy(candy.position)

        self.__candiesField.reduceAllCandiesSizeByOne()

    def __getNextHeadDirection(
        self,
        directionFromKeyboard: Optional[Direction]
    ) -> Direction:
        if (
            (
                self.__snake.headDirection in HORIZONTAL_DIRECTIONS
                and directionFromKeyboard in HORIZONTAL_DIRECTIONS
            ) or (
                self.__snake.headDirection in VERTICAL_DIRECTIONS
                and directionFromKeyboard in VERTICAL_DIRECTIONS
            ) or (
                directionFromKeyboard is None
            )
        ):
            return self.__snake.headDirection

        return directionFromKeyboard

    def __renderCell(
        self,
        position: Position,
        overridedCellKind: Optional[GameCellKind] = None,
        cellRenderer: str = CELL_RENDERER
    ):
        cellKind: GameCellKind = (
            overridedCellKind
            or self.__snake.getGameCellKindBy(position)
            or self.__candiesField.getGameCellKindBy(position)
            or GameCellKind.VOID
        )

        if cellRenderer == 'asset':
            return self.__windowController.drawAsset(
                getAssetForCell(cellKind),
                position
            )

        if cellRenderer == 'color':
            return self.__windowController.drawColor(
                getColorForCell(cellKind),
                position
            )

        raise BrokenGameLogicException('Unknown CELL_RENDERER')

    def __willSnakeStepOutOfGameField(self, direction: Direction):
        position = self.__snake.headPosition.getNewPositionShiftedInto(
            direction
        )
        return (
            position.x < 0
            or position.y <= 0
            or position.x >= GAME_GRID_X_SIZE_IN_GAME_CELLS
            or position.y > GAME_GRID_Y_SIZE_IN_GAME_CELLS
        )

    def __setInitialGameState(self):
        self.__snake = Snake()
        self.__candiesField = CandyMap()
        candy = self.__candiesField.createNewCandy(
            Position(3, 4),
            CandyColor.BLUE,
            7
        )
        self.__renderCell(candy.position)
        candy = self.__candiesField.createNewCandy(
            Position(5, 7),
            CandyColor.RED,
            7
        )
        self.__renderCell(candy.position)
        candy = self.__candiesField.createNewCandy(
            Position(2, 9),
            CandyColor.YELLOW,
            7
        )
        self.__renderCell(candy.position)
        self.__playerScore: int = 0
