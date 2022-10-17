import sys
from typing import Optional
from candy import Candy
from customExceptions import GameOverException, WillingExitException
from direction import Direction
from gameCellKind import GameCellKind
from getAssetForCell import getColorForCell
from position import Position
from snake import Snake
from candyMap import CandyMap
import pygame
from constant import GAME_OVER_BACKGROUND_COLOR, \
    DIFFICULTY, GAME_FIELD_BACKGROUND_COLOR, GAME_OVER_TEXT_COLOR, \
    SNAKE_BODY_COLOR, WINDOW_SIZE_X, WINDOW_SIZE_Y


class GameEngine:
    def __init__(self):
        self.__setInitialGameState()
        self.__initPyGame()

    def runGameLoop(self):
        while True:

            self.__gameWindow.fill(GAME_FIELD_BACKGROUND_COLOR)

            self.__makeGameIteration()

            pygame.display.update()

            self.__gameClock.tick(DIFFICULTY)

    def __makeGameIteration(self):
        self.__makeSnakeIteration(
            self.__snake.getNextHeadDirection(
                self.__parsePyGameEvents()
            )
        )

    def __makeSnakeIteration(self, direction: Direction):
        if not self.__snake.isHeadMovePossibleTo(direction):
            raise GameOverException('Head tried to eat body of the snake')

        doesHeadFacesCandy = self.__doesHeadFacesCandy(direction)

        self.__snake.makeStep(direction, doesHeadFacesCandy)

        if doesHeadFacesCandy:
            candy: Candy = self.__candiesField.getCandyBy(
                self.__snake.headPosition
            )    # type: ignore
            self.__playerScore += candy.size
            self.__candiesField.removeCandyBy(candy.position)

        self.__candiesField.reduceAllCandiesSizeByOne()

    def __renderCell(self, position: Position):
        cellKind: GameCellKind = GameCellKind.VOID
        # getAssetForCell(cellKind=GameCellKind.head_to_BOTTOM)
        pygame.draw.rect(
            self.__gameWindow,
            getColorForCell(cellKind),
            [position.x, position.y, position.x + 1, position.x + 1]
        )
        ...

    def __doesHeadFacesCandy(self, direction: Direction) -> bool:
        return self.__candiesField.getCandyBy(
            self.__snake.headPosition.getNewPositionBy(direction)
        ) is None

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

    def __parsePyGameEvents(self) -> Optional[Direction]:
        direction: Optional[Direction] = None
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
