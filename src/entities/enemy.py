from utils.constants import *

from term import Terminal, TermSprite
from world import *
from utils.int_vect import Int_Vector
from entities.player import Player

class Enemy():
    def __init__(self, char: str, color: TermColor, position: Int_Vector, term: Terminal, level: World) -> None:
        self._term = term
        self._level = level
        self._position = position
        screen_pos = level.world_coord_to_screen_cord(position)
        self._sprite = TermSprite.fromSingleChar(char, color=color, position=screen_pos)

    def update(self, shouldUpdate: bool, player: Player) -> None:
        pass

    def render(self) -> None:
        screen_pos = self._level.world_coord_to_screen_cord(self._position)
        self._sprite.setPosition(screen_pos)
        self._term.draw_term_sprite(self._sprite)
