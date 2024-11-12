import pygame
from enum import Enum

class KeyState(Enum):
    PRESSED = 0
    IDLE = 1
    RELEASED = 2

type KeyStateList = dict[int, KeyState]

class Keyboard():
    def __init__(self) -> None:
        pygame.key.set_repeat(150)
        self._state = dict()
    
    def update(self) -> None:
        # always reset state
        for key in self._state.keys():
            self._state[key] = KeyState.IDLE

        for event in pygame.event.get(pygame.KEYDOWN):
            key = event.dict["key"]
            self._state[key] = KeyState.PRESSED
        for event in pygame.event.get(pygame.KEYUP):
            key = event.dict["key"]
            self._state[key] = KeyState.RELEASED

    def pressed(self, key: int) -> bool:
        if key in self._state:
            return self._state[key] == KeyState.PRESSED
    
    def released(self, key: int) -> bool:
        if key in self._state:
            return self._state[key] == KeyState.RELEASED
