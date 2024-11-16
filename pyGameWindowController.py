import sys
from typing import Optional, Tuple
from customExceptions import WillingExitException, \
    NoPredefinedStepsLeftException
from direction import Direction
from position import Position
import pygame
from pygame import surface, color, rect
from constant import CELL_SIZE_IN_PIXELS, SPEED, GREEN, WHITE, \
    WINDOW_SIZE_Y, \
    GAME_FIELD_BACKGROUND_COLOR, GAME_OVER_TEXT_COLOR, USE_PREDEFINED_STEPS, \
    WINDOW_SIZE_X, GAME_OVER_BACKGROUND_COLOR, changeablePredefinedSteps


class PyGameWindowController:
    def __init__(self):
        self.__initPyGame()

    def updadeScreen(self, *rectsToRerender: rect.Rect):
        pygame.display.update(list(rectsToRerender))
        self.__gameClock.tick(SPEED)

    def drawAsset(self, sourceAsset: surface.Surface, position: Position):
        assetRect = sourceAsset.get_rect(**self.__getCellRectFrom(position))
        return self.__gameWindow.blit(sourceAsset, assetRect)

    def drawColor(self, color: color.Color, position: Position):
        return pygame.draw.rect(
            self.__gameWindow,
            color,
            tuple(self.__getCellRectFrom(position).values())
        )

    def drawWhiteTextOnCell(self, text: str, position: Position):
        my_font = pygame.font.SysFont('verdana', 24)
        game_over_surface = my_font.render(text, True, WHITE)
        game_over_rect = game_over_surface.get_rect(
            **self.__getCellRectFrom(position)
        )
        # game_over_rect.midtop = (
        #     int(WINDOW_SIZE_X / 2),
        #     int(WINDOW_SIZE_Y / 4)
        # )
        return self.__gameWindow.blit(game_over_surface, game_over_rect)

    def renderGameOverScreen(
        self,
        deathReason: str,
        playerScore: int,
        snakeLength: int
    ):
        self.__gameWindow.fill(GAME_OVER_BACKGROUND_COLOR)

        for text, color, font, fontSize, midtop in (
            ('GAME OVER',                   GAME_OVER_TEXT_COLOR, 'times new roman', 90, (int(WINDOW_SIZE_X / 2), int(WINDOW_SIZE_Y / 4   ))),
            (f'Score: {playerScore}',       WHITE,                'times new roman', 26, (int(WINDOW_SIZE_X / 2), int(WINDOW_SIZE_Y / 1.25))),
            (f'Snake lengh: {snakeLength}', GREEN,                'times new roman', 26, (int(WINDOW_SIZE_X / 2), int(WINDOW_SIZE_Y / 1.35))),
            (deathReason,                   GAME_OVER_TEXT_COLOR, 'verdana',         30, (int(WINDOW_SIZE_X / 2), int(WINDOW_SIZE_Y / 1.65)))
        ):
            self.__renderCenteredText(text, color, font, fontSize, midtop)

        pygame.display.update()

    def clearWindow(self):
        self.__gameWindow.fill(GAME_FIELD_BACKGROUND_COLOR)
        pygame.display.update()

    def parsePyGameEvents(self) -> Optional[Direction]:
        direction: Optional[Direction] = None

        if USE_PREDEFINED_STEPS:
            if not changeablePredefinedSteps:
                raise NoPredefinedStepsLeftException()
            return changeablePredefinedSteps.pop(0)

        # parsing all last events at once, so if user changed their mind
        # about snake's direction mid-frame and clicked 2 opposite arrows,
        # only the last press will be interpreted
        for event in pygame.event.get():
            match [event.key if event.type == pygame.KEYDOWN else event.type]:
                case [pygame.QUIT]:
                    raise WillingExitException()
                case [pygame.K_LEFT]:  direction = Direction.LEFT
                case [pygame.K_RIGHT]: direction = Direction.RIGHT
                case [pygame.K_UP]:    direction = Direction.TOP
                case [pygame.K_DOWN]:  direction = Direction.BOTTOM

        return direction

    def renderScoreIntoGameWindow(self, score: int):
        return self.__renderCenteredText(
            f'Score: {score}',
            WHITE,
            'times new roman',
            20,
            (int(WINDOW_SIZE_X / 10), 15)
        )

    def __renderCenteredText(
        self,
        text:  str,
        color: color.Color,
        font: str,
        fontSize: int,
        midtop: Tuple[int, int]
    ):
        score_font = pygame.font.SysFont(font, fontSize)
        score_surface = score_font.render(
            text, True, color, GAME_FIELD_BACKGROUND_COLOR
        )
        score_rect = score_surface.get_rect()
        score_rect.midtop = midtop
        return self.__gameWindow.blit(score_surface, score_rect)

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
        self.clearWindow()

    def __getCellRectFrom(self, position: Position):
        return {
            'x': position.x * CELL_SIZE_IN_PIXELS,
            # needed because pygame has coordinates system with reversed Y
            'y': WINDOW_SIZE_Y - (position.y + 1) * CELL_SIZE_IN_PIXELS,
            'width': CELL_SIZE_IN_PIXELS,
            'height': CELL_SIZE_IN_PIXELS
        }
