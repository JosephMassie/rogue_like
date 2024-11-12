import os

from term import *
from utils.int_vect import Int_Vector
from utils.input import Keyboard

class World():
    def __init__(
            self,
            filePath: str,
            term: Terminal,
            keyboard: Keyboard,
            ) -> None:
        self._term = term
        self._keyboard = keyboard
        with open(filePath) as file:
            data = file.read()
            data = data.splitlines()

            self._grid: TermCharBuff = []
            for line in data:
                self._grid.append(list(line))
        self._camera_pos = Int_Vector(0, 0)
    
    def _cut_to_camera(self) -> TermCharBuff:
        screen_width = self._term.get_width()
        screen_height = self._term.get_height()

        grid: TermCharBuff = []
        grid_max_height = len(self._grid)
        grid_max_width = get_char_buff_width(self._grid)

        cam_x, cam_y = self._camera_pos.getCoords()
        buff_height = cam_y + screen_height
        if buff_height > grid_max_height:
            buff_height = grid_max_height
        buff_width = cam_x + screen_width
        if buff_width > grid_max_width:
            buff_width = grid_max_width

        for i in range(cam_y, buff_height):
            grid.append(self._grid[i][cam_x:buff_width])
        return grid

    def move_camera(self, direction: Int_Vector) -> None:
        self._camera_pos = self._camera_pos + direction
        x, y = self._camera_pos.getCoords()
        if x < 0:
            x = 0
        if y < 0:
            y = 0
        self._camera_pos.setCoords((x, y))
    
    def update(self) -> None:
        directions = [
            (pygame.K_w, (0, -1)),
            (pygame.K_a, (-1, 0)),
            (pygame.K_s, (0, 1)),
            (pygame.K_d, (1, 0))
        ]

        for key, dir in directions:
            if self._keyboard.pressed(key):
                delta = Int_Vector(*dir)
                self.move_camera(delta)
    
    def render(self) -> None:
        frame: TermContent = {
            "chars": self._cut_to_camera()
        }
        self._term.draw_element(frame, 0, 0)
    
    def world_coord_to_screen_cord(self, position: Int_Vector) -> Int_Vector:
        spos = position - self._camera_pos
        #print(f"{position} - {self._camera_pos} = {spos}")
        return spos
