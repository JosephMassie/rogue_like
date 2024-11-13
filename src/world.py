from __future__ import annotations

from term import *
from utils.int_vect import Int_Vector
from utils.input import Keyboard

from enum import *

@unique
class CellType(Enum):
    START = auto()
    EMPTY = auto()
    WALL = auto()
    FLOOR = auto()
    DOOR = auto()
    WATER = auto()
    GRASS = auto()
    TREE = auto()

class Cell():
    def __init__(self, display_char: str, type: CellType, colors: tuple[pygame.Color, pygame.Color], passable: bool = True) -> None:
        self._char = display_char
        self._type = type
        self._colors = colors
        self.passable = passable
    
    @classmethod
    def from_character(_, char: str) -> Cell:
        type: CellType = None
        colors: tuple[pygame.Color, pygame.Color] = None
        passable = True

        match char:
            case "S":
                char = "."
                type = CellType.START
                colors = (pygame.Color("#17161c"), pygame.Color("#39383f"))
            case ".":
                type = CellType.FLOOR
                colors = (pygame.Color("#17161c"), pygame.Color("#39383f"))
            case "#":
                type = CellType.WALL
                colors = (pygame.Color("#4d5f60"), pygame.Color("#273a44"))
                passable = False
            case '"':
                type = CellType.GRASS
                colors = (pygame.Color("#206d0a"), pygame.Color("#143f08"))
            case "^":
                type = CellType.TREE
                colors = (pygame.Color("#043a0d"), pygame.Color("#05891b"))
                passable = False
            case "~":
                type = CellType.WATER
                colors = (pygame.Color("#083f3c"), pygame.Color("#08263f"))
                passable = False
            case "D":
                type = CellType.DOOR
                colors = (pygame.Color("#684a33"), pygame.Color("#331d0c"))
            case " " | "\n":
                char = " "
                type = CellType.EMPTY
                colors = (DEFAULT_BG_COLOR, DEFAULT_FG_COLOR)
            case _:
                print(f"creating Cell from unknown character '{char}'")
                type = CellType.EMPTY
                colors = (DEFAULT_BG_COLOR, DEFAULT_FG_COLOR)
        return Cell(char, type, colors, passable)

type WorldGrid = list[list[Cell]]

class World():
    def __init__(
            self,
            filePath: str,
            term: Terminal,
            keyboard: Keyboard,
            ) -> None:
        self._term = term
        self._keyboard = keyboard
        
        self._build_from_file(filePath)
        self._height = len(self._grid)
        self._width = get_2d_grid_width(self._grid)
        self._camera_pos = Int_Vector(0, 0)
    
    def _build_from_file(self, filePath: str):
        with open(filePath) as file:
            data = file.readlines()

            self._grid: WorldGrid = []
            for y in range(len(data)):
                line = data[y]
                row: list[Cell] = []
                for x in range(len(line)):
                    char = line[x]
                    cell = Cell.from_character(char)
                    row.append(cell)
                    if cell._type == CellType.START:
                        self._player_spawn = Int_Vector(x, y)
                self._grid.append(row)
    
    def get_player_spawn(self) -> Int_Vector:
        if isinstance(self._player_spawn, Int_Vector):
            return self._player_spawn
        else:
            return Int_Vector(1, 1)
    
    def is_passable(self, position: Int_Vector) -> CellType:
        x, y = position.getCoords()
        if x < 0 or x >= self._width or y < 0 or y >= self._height:
            return False
        return self._grid[y][x].passable

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
    
    def _grid_to_content_for_camera(self) -> TermContent:
        screen_width = self._term.get_width()
        screen_height = self._term.get_height()

        content: TermContent = {
            "chars": [],
            "colors": []
        }
        grid_max_height = len(self._grid)
        grid_max_width = get_2d_grid_width(self._grid) - 1

        cam_x, cam_y = self._camera_pos.getCoords()

        buff_height = cam_y + screen_height
        if buff_height > grid_max_height:
            buff_height = grid_max_height
        buff_width = cam_x + screen_width
        if buff_width > grid_max_width:
            buff_width = grid_max_width

        for y in range(cam_y, buff_height):
            char_row: list[str] = []
            color_row: list[tuple[pygame.Color, pygame.Color]] = []
            for x in range(cam_x, buff_width):
                cell: Cell = None
                if x >= len(self._grid[y]):
                    cell = Cell.from_character(" ")
                else:
                    cell = self._grid[y][x]
                char_row.append(cell._char)
                color_row.append(cell._colors)
            content["chars"].append(char_row)
            content["colors"].append(color_row)

        return content
    
    def render(self) -> None:
        frame = self._grid_to_content_for_camera()
        self._term.draw_content(frame, 0, 0)
    
    def world_coord_to_screen_cord(self, position: Int_Vector) -> Int_Vector:
        return position - self._camera_pos
