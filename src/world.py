import os

from term import *

class World():
    def __init__(self, filePath: str, term: Terminal) -> None:
        self._term = term
        with open(filePath) as file:
            data = file.read()
            data = data.splitlines()

            self._grid: TermCharBuff = []
            for line in data:
                self._grid.append(list(line))
        self._camera_x = 0
        self._camera_y = 0
    
    def _cut_to_camera(self) -> TermCharBuff:
        screen_width = self._term.get_width()
        screen_height = self._term.get_height()

        grid: TermCharBuff = []
        grid_max_height = len(self._grid)
        grid_max_width = get_char_buff_width(self._grid)

        buff_height = self._camera_y + screen_height
        if buff_height > grid_max_height:
            buff_height = grid_max_height
        buff_width = self._camera_x + screen_width
        if buff_width > grid_max_width:
            buff_width = grid_max_width

        for i in range(self._camera_y, buff_height):
            grid.append(self._grid[i][self._camera_x:buff_width])
        return grid

    def move_camera(self, x: int, y: int) -> None:
        self._camera_x += x
        if self._camera_x < 0:
            self._camera_x = 0
        self._camera_y += y
        if self._camera_y < 0:
            self._camera_y = 0
    
    def render(self) -> None:
        frame: TermContent = {
            "chars": self._cut_to_camera()
        }
        self._term.draw_element(frame, 0, 0)
    
    def world_coord_to_screen_cord(self, x: int, y: int) -> tuple[int, int]:
        return x - self._camera_x, y - self._camera_y
