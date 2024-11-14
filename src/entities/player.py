import pygame

from utils.constants import *

from term import Terminal, TermSprite
from world import *
from utils.input import Keyboard
from utils.int_vect import Int_Vector

class Player():
    def __init__(self, position: Int_Vector, term: Terminal, level: World, keyboard: Keyboard) -> None:
        self._term = term
        self._level = level
        self._keyboard  = keyboard

        self._position = position
        screen_pos = self._level.world_coord_to_screen_cord(position)
        self._sprite = TermSprite.fromSingleChar("@", color=(None, pygame.Color(0, 150, 0)), position=screen_pos)
    
    def render(self):
        screen_pos = self._level.world_coord_to_screen_cord(self._position)
        self._sprite.setPosition(screen_pos)
        self._term.draw_term_sprite(self._sprite)
    
    def set_position(self, position: Int_Vector):
        self._position = position
    
    def get_position(self) -> Int_Vector:
        return self._position
    
    def move(self, delta: Int_Vector):
        pos = self._position + delta
        if not self._level.is_passable(pos):
            return
        self._position = pos
    
    # processes player input and updates their state accordingly
    #  returns true if any state was updated and false otherwise
    def update(self) -> bool:
        directions = [
            (pygame.K_UP, (0, -1)),
            (pygame.K_DOWN, (0, 1)),
            (pygame.K_LEFT, (-1, 0)),
            (pygame.K_RIGHT, (1, 0))
        ]

        updateOccurred = False
        for key, dir in directions:
            if self._keyboard.pressed(key):
                delta = Int_Vector(*dir)
                self.move(delta)
                updateOccurred = True
        return updateOccurred
