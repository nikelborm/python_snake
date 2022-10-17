import sys
import pygame
from gameEngine import GameEngine
from customExceptions import GameOverException, WillingExitException

# 2    *    *    *
#
# 1    *    *    *
#
# 0    *    *    *
# ^
# y
# x->0    1    2


if __name__ == "__main__":
    game = GameEngine()
    try:
        game.runGameLoop()
        # pass
    except (
        GameOverException, WillingExitException, KeyboardInterrupt
    ) as error:
        print(error)
        pygame.quit()
        sys.exit()
