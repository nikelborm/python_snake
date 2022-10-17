import sys
from typing import Optional
from customExceptions import WillingExitException, \
    NoPredefinedStepsLeftException
from direction import Direction
from position import Position
import pygame
from pygame import surface, color
from constant import CELL_SIZE_IN_PIXELS, DIFFICULTY, WINDOW_SIZE_Y, \
    GAME_FIELD_BACKGROUND_COLOR, GAME_OVER_TEXT_COLOR, USE_PREDEFINED_STEPS, \
    WINDOW_SIZE_X, GAME_OVER_BACKGROUND_COLOR, changeblePredefinedSteps


class PyGameWindowController:
    def __init__(self):
        self.__initPyGame()

    def updadeScreen(self, *positionsOfScreenToUpdate: Position):
        pygame.display.update()
        self.__gameClock.tick(DIFFICULTY)

    def drawAsset(self, sourceAsset: surface.Surface, position: Position):
        assetRect = sourceAsset.get_rect(**self.__getCellRectFrom(position))
        return self.__gameWindow.blit(sourceAsset, assetRect)

    def drawColor(self, color: color.Color, position: Position):
        return pygame.draw.rect(
            self.__gameWindow,
            color,
            tuple(self.__getCellRectFrom(position).values())
        )

    def renderGameOverScreen(self, score):
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
        self.renderScore(score, 0, GAME_OVER_TEXT_COLOR, 'times', 20)
        pygame.display.flip()

    def parsePyGameEvents(self) -> Optional[Direction]:
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

    def renderScore(self, score, choice, color, font, size):
        score_font = pygame.font.SysFont(font, size)
        score_surface = score_font.render(
            f'Score : {score}',
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

    def __getCellRectFrom(self, position: Position):
        return {
            'x': position.x * CELL_SIZE_IN_PIXELS,
            # needed because pygame has coordinates system with reversed Y
            'y': WINDOW_SIZE_Y - position.y * CELL_SIZE_IN_PIXELS,
            'width': CELL_SIZE_IN_PIXELS,
            'height': CELL_SIZE_IN_PIXELS
        }
