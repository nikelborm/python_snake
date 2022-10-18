import random
from typing import Optional
from candy import Candy
from candyColor import ALL_CANDY_COLORS, CandyColor
from customExceptions import BrokenGameLogicException, GameOverException
from direction import HORIZONTAL_DIRECTIONS, VERTICAL_DIRECTIONS, Direction
from gameCellKind import CANDY_SET, GameCellKind
from getAssetForCell import getAssetForCell, getColorForCell
from position import Position
from pyGameWindowController import PyGameWindowController
from snake import Snake
from pygame import rect
from candyMap import CandyMap
from constant import ALL_POSSIBLE_POSITIONS, CELL_RENDERER, \
    GAME_GRID_Y_SIZE_IN_GAME_CELLS, GAME_GRID_X_SIZE_IN_GAME_CELLS
from soundProcessing import SoundKind, getSoundBy


class GameEngine:
    def __init__(self):
        self.__windowController = PyGameWindowController()
        self.__playerScore: int = 0
        self.__snakeLength: int = 0

    def runGameLoop(self):
        self.__windowController.clearWindow()
        self.__setInitialGameState()
        while True:
            rectsToRerender = self.__makeGameIteration(
                self.__getNextHeadDirection(
                    self.__windowController.parsePyGameEvents()
                )
            )

            self.__windowController.updadeScreen(*rectsToRerender)
            # pass

    def renderGameOverScreen(self, deathReason: str):
        self.__windowController.renderGameOverScreen(
            deathReason,
            self.__playerScore,
            self.__snakeLength
        )

    def __makeGameIteration(self, direction: Direction):
        if self.__snake.willSnakeBiteItselfAfterMove(direction):
            raise GameOverException('Snake tried to bite itself')

        if self.__willSnakeStepOutOfGameField(direction):
            raise GameOverException('Snake tried to bite border of game field')

        candy = self.__candiesField.getCandyBy(
            self.__snake.headPosition.getNewPositionShiftedInto(direction)
        )
        doesHeadFacesCandy = candy is not None
        if doesHeadFacesCandy:
            getSoundBy(SoundKind.CANDY_EATEN).play()

        return [
            *(
                self.__renderCell(position)
                for position in self.__snake.makeStepAndGetPositionsToRerender(
                    direction,
                    doesHeadFacesCandy
                )
            ),
            *self.__makeGameIterationForCandies(
                candy,
            )
        ]

    def __makeGameIterationForCandies(
        self,
        candy: Optional[Candy],
    ):
        doesHeadFacesCandy = candy is not None
        if doesHeadFacesCandy:
            self.__playerScore += candy.size
            self.__snakeLength += 1
            self.__candiesField.removeCandyBy(candy.position)

        removedCandyPositions = self.__candiesField.reduceAllCandiesSizeByOne()

        if doesHeadFacesCandy:
            removedCandyPositions.append(candy.position)

        return [
            *(self.__renderCell(candy.position)
                for candy in self.__candiesField.getAllCandies()),

            *(self.__renderCell(position)
                for position in removedCandyPositions),

            *(self.__renderCell(self.__generateCandy().position)
                for _ in removedCandyPositions)
        ]

    def __generateCandy(self):
        position = random.choice(tuple(
            ALL_POSSIBLE_POSITIONS
            - {candy.position for candy in self.__candiesField.getAllCandies()}
            - set(self.__snake.allNodesPositions)
        ))
        snakeWayToReachPosition = (
            abs(position.x - self.__snake.headPosition.x)
            + abs(position.y - self.__snake.headPosition.y)
        )
        return self.__candiesField.createNewCandy(
            position,
            random.choice(ALL_CANDY_COLORS),
            int(snakeWayToReachPosition * 1.2)
            + random.randrange(10)
            + 1
        )

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
        cellKind: GameCellKind = self.__getCellKindBy(
            position,
            overridedCellKind
        )
        rectToRerender: Optional[rect.Rect] = None

        if cellRenderer == 'color':
            rectToRerender = self.__windowController.drawColor(
                getColorForCell(cellKind),
                position
            )
        elif cellRenderer == 'asset':
            rectToRerender = self.__windowController.drawAsset(
                getAssetForCell(cellKind),
                position
            )

        if cellKind in CANDY_SET:
            candy: Candy = self.__candiesField.getCandyBy(
                position)  # type: ignore
            self.__windowController.drawWhiteTextOnCell(
                f'{candy.size}',
                position
            )
        if rectToRerender:
            return rectToRerender
        else:
            raise BrokenGameLogicException('Unknown CELL_RENDERER')

    def __willSnakeStepOutOfGameField(self, direction: Direction):
        position = self.__snake.headPosition.getNewPositionShiftedInto(
            direction
        )
        return (
            position.x < 0
            or position.y < 0
            or position.x >= GAME_GRID_X_SIZE_IN_GAME_CELLS
            or position.y >= GAME_GRID_Y_SIZE_IN_GAME_CELLS
        )

    def __getCellKindBy(
        self,
        position: Position,
        overridedCellKind: Optional[GameCellKind] = None,
    ):
        return (
            overridedCellKind
            or self.__snake.getGameCellKindBy(position)
            or self.__candiesField.getGameCellKindBy(position)
            or GameCellKind.VOID
        )

    def __setInitialGameState(self):
        self.__snake = Snake()
        self.__candiesField = CandyMap()
        candies = [
            self.__candiesField.createNewCandy(
                Position(3, 4),
                CandyColor.BLUE,
                5
            ),
            self.__candiesField.createNewCandy(
                Position(5, 7),
                CandyColor.RED,
                9
            ),
            self.__candiesField.createNewCandy(
                Position(2, 9),
                CandyColor.YELLOW,
                15
            )
        ]
        self.__windowController.updadeScreen(
            *(self.__renderCell(candy.position) for candy in candies),
            *(self.__renderCell(position)
                for position in self.__snake.allNodesPositions)
        )
        self.__playerScore: int = 0
        self.__snakeLength: int = 3
