from utils.constants import *

from term import Terminal, TermSprite
from world import *
from utils.int_vect import *
from entities.player import Player

class Enemy():
    def __init__(self, char: str, color: TermColor, position: Int_Vector, term: Terminal, level: World, player: Player) -> None:
        self._term = term
        self._level = level
        self._position = position
        screen_pos = level.world_coord_to_screen_cord(position)
        self._sprite = TermSprite.fromSingleChar(char, color=color, position=screen_pos)
        self._level = level
        self._player = player

    def update(self, shouldUpdate: bool):
        if not shouldUpdate:
            return
        path = self._level.getPath(self._position, self._player.get_position())
        distance = len(path)
        if distance > 2 and distance < 10:
            self._position = path[1]
        

    def render(self) -> None:
        screen_pos = self._level.world_coord_to_screen_cord(self._position)
        self._sprite.setPosition(screen_pos)
        self._term.draw_term_sprite(self._sprite)

    def get_position(self) -> Int_Vector:
        return self._position
