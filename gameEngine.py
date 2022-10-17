import sys
from typing import Optional
from candy import Candy
from candyColor import CandyColor
from customExceptions import GameOverException, WillingExitException,\
    NoPredefinedStepsLeftException
from direction import HORIZONTAL_DIRECTIONS, VERTICAL_DIRECTIONS, Direction
from gameCellKind import GameCellKind
from getAssetForCell import getColorForCell
from position import Position
from snake import Snake
from candyMap import CandyMap
import pygame
from constant import CELL_SIZE_IN_PIXELS, GAME_GRID_X_SIZE_IN_GAME_CELLS, \
    GAME_GRID_Y_SIZE_IN_GAME_CELLS, GAME_OVER_BACKGROUND_COLOR, \
    DIFFICULTY, GAME_FIELD_BACKGROUND_COLOR, changeblePredefinedSteps,\
    GAME_OVER_TEXT_COLOR, USE_PREDEFINED_STEPS, WINDOW_SIZE_X, WINDOW_SIZE_Y


class GameEngine:
    def __init__(self):
        self.__initPyGame()
        self.__setInitialGameState()

    def runGameLoop(self):
        while True:
            self.__makeGameIteration()

            pygame.display.update()

            self.__gameClock.tick(DIFFICULTY)

    def __makeGameIteration(self):
        self.__makeSnakeIteration(
            self.__getNextHeadDirection(
                self.__parsePyGameEvents()
            )
        )

    def __makeSnakeIteration(self, direction: Direction):
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

        for position in cellsPositions:
            self.__renderCell(position)

        if doesHeadFacesCandy:
            self.__playerScore += candy.size
            self.__candiesField.removeCandyBy(candy.position)

        self.__candiesField.reduceAllCandiesSizeByOne()

    def __renderCell(
        self,
        position: Position,
        overridedCellKind: Optional[GameCellKind] = None
    ):
        print(f'{position}_{self.__candiesField.getGameCellKindBy(position)}')
        cellKind: GameCellKind = (
            overridedCellKind
            or self.__snake.getGameCellKindBy(position)
            or self.__candiesField.getGameCellKindBy(position)
            or GameCellKind.VOID
        )

        pygame.draw.rect(
            self.__gameWindow,
            getColorForCell(cellKind),
            pygame.Rect(
                position.x * CELL_SIZE_IN_PIXELS,
                WINDOW_SIZE_Y - position.y * CELL_SIZE_IN_PIXELS,
                CELL_SIZE_IN_PIXELS,
                CELL_SIZE_IN_PIXELS
            )
        )

    def __renderVoidCell(self, position: Position):
        self.__renderCell(position, GameCellKind.VOID)

    def __renderGameOverScreen(self):
        my_font = pygame.font.SysFont('times new roman', 90)
        game_over_surface = my_font.render(
            'GAME OVER',
            True,
            GAME_OVER_TEXT_COLOR
        )
        game_over_rect = game_over_surface.get_rect()
        game_over_rect.midtop = (
            int(WINDOW_SIZE_X / 2),
            int(WINDOW_SIZE_Y / 4)
        )
        self.__gameWindow.fill(GAME_OVER_BACKGROUND_COLOR)
        self.__gameWindow.blit(game_over_surface, game_over_rect)
        self.__renderScore(0, GAME_OVER_TEXT_COLOR, 'times', 20)
        pygame.display.flip()
        # time.sleep(3)
        # pygame.quit()
        # sys.exit()

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

    def __renderScore(self, choice, color, font, size):
        score_font = pygame.font.SysFont(font, size)
        score_surface = score_font.render(
            f'Score : {self.__playerScore}',
            True,
            color
        )
        score_rect = score_surface.get_rect()
        if choice == 1:
            score_rect.midtop = (int(WINDOW_SIZE_X / 10), 15)
        else:
            score_rect.midtop = (
                int(WINDOW_SIZE_X / 2),
                int(WINDOW_SIZE_Y / 1.25)
            )
        self.__gameWindow.blit(score_surface, score_rect)

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

    def __parsePyGameEvents(self) -> Optional[Direction]:
        direction: Optional[Direction] = None

        if USE_PREDEFINED_STEPS:
            if not changeblePredefinedSteps:
                raise NoPredefinedStepsLeftException()
            return changeblePredefinedSteps.pop(0)

        for event in pygame.event.get():
            match [event.key if event.type == pygame.KEYDOWN else event.type]:
                case [pygame.QUIT]:
                    raise WillingExitException()
                case [pygame.K_LEFT]:  direction = Direction.LEFT
                case [pygame.K_RIGHT]: direction = Direction.RIGHT
                case [pygame.K_UP]:    direction = Direction.TOP
                case [pygame.K_DOWN]:  direction = Direction.BOTTOM
        return direction

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

    def __initPyGame(self):
        check_errors = pygame.init()
        if check_errors[1] > 0:
            print(
                f'[!] Had {check_errors[1]} errors when game init, exiting...'
            )
            sys.exit(-1)
        else:
            print('[+] Game successfully initialised')

        pygame.display.set_caption('Snake game made by nikelborm')
        self.__gameWindow = pygame.display.set_mode(
            (WINDOW_SIZE_X, WINDOW_SIZE_Y)
        )
        self.__gameClock = pygame.time.Clock()
        self.__gameWindow.fill(GAME_FIELD_BACKGROUND_COLOR)
