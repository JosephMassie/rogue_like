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
        if self._level.is_passable(pos) == False:
            return
        self._position = pos
    
    # processes player input and updates their state accordingly
    #  returns true if any state was updated and false otherwise
    def update(self) -> bool:
        directions = [
            (pygame.K_UP, UP),
            (pygame.K_DOWN, DOWN),
            (pygame.K_LEFT, LEFT),
            (pygame.K_RIGHT, RIGHT)
        ]

        updateOccurred = False
        for key, dir in directions:
            if self._keyboard.pressed(key):
                self.move(dir)
                updateOccurred = True

        screen_pos = self._level.world_coord_to_screen_cord(self._position)
        x, y = screen_pos.getCoords()
        screen_width = self._term.get_width() - PLAYER_SCREEN_BUFFER
        screen_height = self._term.get_height() - PLAYER_SCREEN_BUFFER

        camera_velocity = Int_Vector(0, 0)

        # if the player moves out of bounds on the screen adjust the camera
        if x < PLAYER_SCREEN_BUFFER:
            camera_velocity += Int_Vector(-1, 0)
        elif x > screen_width:
            camera_velocity += Int_Vector(1, 0)
        
        if y < PLAYER_SCREEN_BUFFER:
            camera_velocity += Int_Vector(0, -1)
        elif y > screen_height:
            camera_velocity += Int_Vector(0, 1)
        
        self._level.move_camera(camera_velocity)

        return updateOccurred
