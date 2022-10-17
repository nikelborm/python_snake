import sys
from time import sleep
import pygame
from gameEngine import GameEngine
from customExceptions import GameOverException, WillingExitException,\
    NoPredefinedStepsLeftException
from soundProcessing import SoundKind, fillSoundStore, getSoundBy

# 2    *    *    *
#
# 1    *    *    *
#
# 0    *    *    *
# ^
# y
# x->0    1    2


if __name__ == "__main__":
    pygame.mixer.init()
    fillSoundStore()
    gameEngine = GameEngine()
    # gameEngine.renderGameOverScreen('You died because you are an idiot')
    # sleep(5)
    while True:
        try:
            gameEngine.runGameLoop()
            # pass
        except (WillingExitException, KeyboardInterrupt) as error:
            print(error)
            break
        except GameOverException as error:
            print(error)
            gameEngine.renderGameOverScreen(error.args[0])
            getSoundBy(SoundKind.GAME_OVER).play()
            sleep(5)
        except NoPredefinedStepsLeftException as error:
            print(error)
            sleep(10)
            break
    pygame.quit()
    sys.exit()
