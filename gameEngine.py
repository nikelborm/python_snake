import sys
from typing import Optional
from customExceptions import GameOverException, WillingExitException
from direction import Direction
from snake import Snake
from candyMap import CandyMap
import pygame
from constant import BLACK, DIFFICULTY, RED, WHITE, WINDOW_SIZE_X, WINDOW_SIZE_Y


class GameEngine:
  def __init__(self):
    self.__snake = Snake()
    self.__candiesField = CandyMap()
    self.__gameScore: int = 0

    self.__initPyGame()
    pygame.display.set_caption('Snake game made by nikelborm')
    self.__gameWindow = pygame.display.set_mode(( WINDOW_SIZE_X, WINDOW_SIZE_Y ))
    self.__gameClock = pygame.time.Clock()

  def startGameLoop(self):
    while True:
      # pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))
      self.__gameWindow.fill(WHITE)
      pygame.draw.rect(self.__gameWindow, BLACK, [1, 1, 10, 10])
      pygame.display.update()
      # Refresh rate
      self.__gameClock.tick(DIFFICULTY)

  def makeGameIteration(self):
    self.makeSnakeIteration(
      self.__snake.getNextHeadDirection(
        self.__parsePyGameEvents()
      )
    )

  def makeSnakeIteration(self, direction: Direction):
    if not self.__snake.isHeadMovePossibleTo(direction):
      raise GameOverException('Head tried to eat body of the snake')

    doesHeadFacesCandy = self.__doesHeadFacesCandy(direction)

    self.__snake.makeStep(direction, doesHeadFacesCandy)

    if doesHeadFacesCandy:
      self.__candiesField.removeCandyBy(self.__snake.headPosition)

    self.__candiesField.reduceAllCandiesSizeByOne()

  def renderFrame(self):
    pass

  def __doesHeadFacesCandy(self, direction: Direction) -> bool:
    return self.__candiesField.getCandyBy(
      self.__snake.headPosition.getNewPositionBy(direction)
    ) is None

  def renderGameOverScreen(self):
    my_font = pygame.font.SysFont('times new roman', 90)
    game_over_surface = my_font.render('YOU DIED', True, RED)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (int(WINDOW_SIZE_X / 2), int(WINDOW_SIZE_Y / 4))
    self.__gameWindow.fill(BLACK)
    self.__gameWindow.blit(game_over_surface, game_over_rect)
    self.show_score(0, RED, 'times', 20)
    pygame.display.flip()
    # time.sleep(3)
    # pygame.quit()
    # sys.exit()

  def show_score(self, choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render(f'Score : {self.__gameScore}', True, color)
    score_rect = score_surface.get_rect()
    if choice == 1:
      score_rect.midtop = (int(WINDOW_SIZE_X / 10), 15)
    else:
      score_rect.midtop = (int(WINDOW_SIZE_X / 2), int(WINDOW_SIZE_Y / 1.25))
    self.__gameWindow.blit(score_surface, score_rect)

  def __parsePyGameEvents(self) -> Optional[Direction]:
    direction: Optional[Direction] = None
    for event in pygame.event.get():
      match [event.key if event.type == pygame.KEYDOWN else event.type]:
        case [pygame.QUIT]:    raise WillingExitException()
        case [pygame.K_LEFT]:  direction = Direction.left
        case [pygame.K_RIGHT]: direction = Direction.right
        case [pygame.K_UP]:    direction = Direction.top
        case [pygame.K_DOWN]:  direction = Direction.bottom
    return direction

  def __initPyGame(self):
    check_errors = pygame.init()
    if check_errors[1] > 0:
      print(f'[!] Had {check_errors[1]} errors when initialising game, exiting...')
      sys.exit(-1)
    else:
      print('[+] Game successfully initialised')
