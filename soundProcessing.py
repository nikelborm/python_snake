from enum import Enum
import os
from pygame import mixer


class SoundKind(Enum):
    GAME_OVER = 1
    CANDY_EATEN = 2


def getSoundBy(soundKind: SoundKind):
    return soundStore[soundKind]


soundStore: dict[SoundKind, mixer.Sound] = {}


def fillSoundStore():
    global soundStore
    soundStore = {
        SoundKind.GAME_OVER: mixer.Sound(
            os.path.join('assetsSounds', 'game_over.mp3')
        ),
        SoundKind.CANDY_EATEN: mixer.Sound(
            os.path.join('assetsSounds', 'eating.wav')
        )
    }
