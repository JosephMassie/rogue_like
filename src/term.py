from __future__ import annotations

import pygame
from pygame.locals import *

from typing import TypedDict, Required, NotRequired

from utils.constants import *
from utils.int_vect import Int_Vector

type TermColor = tuple[pygame.Color | None, pygame.Color | None]
type TermCharBuff = list[list[str]]
type TermColorBuff = list[list[TermColor]]

class TermContent(TypedDict):
    chars: Required[TermCharBuff]
    colors: NotRequired[TermColorBuff]

def get_2d_grid_width(buffer: list[list[any]]) -> int:
    greatest_width = 0
    for row in buffer:
        width = len(row)
        if width > greatest_width:
            greatest_width = width
    return greatest_width

def get_clean_content(elem: TermContent) -> TermContent:
    chars = elem["chars"].copy()
    for i in range(len(elem["chars"])):
        old_row = elem["chars"][i]
        row = []
        for piece in old_row:
            if isinstance(piece, str):
                row += list(piece)
            else:
                row.append(piece)
        chars[i] = row
    return chars

class TermSprite():
    def __init__(self, content: TermContent, position: Int_Vector) -> None:
        self.content = content
        self.pos =  position
    
    def setPosition(self, position: Int_Vector) -> None:
        self.pos = position
    
    def fillContent(self, content: str, width: int = 1, height: int = 1) -> None:
        self.content["chars"] = [[content for _ in range(width)] for _ in range(height)]
        # clamp down colors to match fill size
        if len(self.content["colors"]) != height or get_2d_grid_width(self.content["colors"]) != width:
            self.content["colors"] = self.content["colors"][:height]
            for i in range(len(self.content["colors"])):
                self.content["colors"][i] = self.content["colors"][i][:width]
    
    @classmethod
    def fromSingleChar(cls, char: str, *, color: TermColor = (None, DEFAULT_FG_COLOR), width: int = 1, height: int = 1, position: Int_Vector = Int_Vector(0, 0)) -> TermSprite | None:
        if len(char) != 1:
            print(f"[TermSprite] invalid char must be a single character")
            return None
        content: TermContent = {
            "chars": [[char for _ in range(width)] for _ in range(height)],
            "colors": [[color for _ in range(width)] for _ in range(height)]
        }
        return TermSprite(content, position)
    
    def fillColor(self, color: pygame.Color, bgcolor: pygame.Color = None) -> None:
        chars = self.content["chars"]
        height = len(chars)
        width = get_2d_grid_width(self.content["chars"])
        colors = [[(bgcolor, color) for _ in range(width)] for _ in range(height)]
        self.content["colors"] = colors

class Terminal():
    # takes in a width and length in character counts
    # creates a pygame screen based on the font_size and
    # those width and height values
    def __init__(
            self,
            width: int,
            height: int,
            font_size: int,
            background_color: pygame.Color = DEFAULT_BG_COLOR,
            gap: int = 10,
            default_color: pygame.Color = DEFAULT_FG_COLOR
            ) -> None:
        self._gap = gap
        self._width = width
        self._height = height
        self._font_size = font_size

        self._bg_color = background_color
        self._default_color = default_color

        self._printer = pygame.font.Font("assets/3270NerdFontMono-Regular.ttf", size=font_size)

        # set initial content to blank spaces
        self.clear_buffer()
        # preform a quick render to get screen width and individual character width
        row_width, self._line_height = self._printer.size("".join(self._content[0]))

        self._char_width = row_width / width
        self._screen_width = row_width + gap * 2
        self._screen_height = height * self._line_height + gap * 2

        print(f"creating a terminal display of [{self._screen_width},{self._screen_height}]")
        self._screen = pygame.display.set_mode((self._screen_width, self._screen_height))
    
    def get_width(self) -> int:
        return self._width
    def get_height(self) -> int:
        return self._height

    def clear_buffer(self) -> None:
        self._content: TermCharBuff = [[BLANK_CELL for _ in range(self._width)] for _ in range(self._height)]
        self._content_color = [[(self._bg_color, self._default_color) for _ in range(self._width)] for _ in range(self._height)]
    
    def draw_line(self, start: Int_Vector, end: Int_Vector, char: str = "?", bg_color: pygame.Color = None, fg_color: pygame.Color = None, mark_ends: bool = False):
        points = start.plot_difference(end)

        if bg_color == None:
            bg_color = self._bg_color
        if fg_color == None:
            fg_color = self._default_color

        color_data = (bg_color, fg_color)

        length = len(points)
        for i in range(length):
            x, y = points[i].getCoords()
            data = char
            if mark_ends:
                if i == 0:
                    data = "$"
                elif i == length - 1:
                    data = "^"
            self._content[y][x] = data
            self._content_color[y][x] = color_data

    def draw_content(self, elem: TermContent, x: int, y: int) -> None:
        if x < 0 or x >= self._width or y < 0 or y >= self._height:
            #print(f"can't draw element out of range, invalid coords [{x},{y}]")
            return
        
        chars = get_clean_content(elem)
        height = len(chars)
        width = get_2d_grid_width(elem["chars"])

        for yy in range(height):
            if yy < self._height:
                for xx in range(len(chars[yy])):
                    if xx < self._width:
                        self._content[y + yy][x + xx] = chars[yy][xx]
        
        if "colors" in elem:
            colors = elem["colors"]
            for yy in range(len(colors)):
                if yy < self._height:
                    for xx in range(len(colors[yy])):
                        if xx < self._width:
                            existing_bg, existing_fg = self._content_color[y + yy][x + xx]
                            new_bg, new_fg = colors[yy][xx]
                            bg = existing_bg if new_bg == None else new_bg
                            fg = existing_fg if new_fg == None else new_fg
                            self._content_color[y + yy][x + xx] = (bg, fg)
        else:
            for yy in range(height):
                if yy < self._height:
                    for xx in range(width):
                        if xx < self._width:
                            self._content_color[y + yy][x + xx] = (self._bg_color, self._default_color)
    
    def draw_term_sprite(self, spr: TermSprite) -> None:
        self.draw_content(spr.content, *spr.pos.getCoords())

    # clear screen and render newly provided content
    def render_buffer(self) -> None:
        self._screen.fill(self._bg_color)
        
        ## Borders to draw for debugging
        """ r = pygame.Rect(self._screen_width-self._gap, self._gap, self._gap, self._screen_height - self._gap*2)
        r2 = pygame.Rect(self._gap, 0, self._screen_width-self._gap*2, self._gap)
        r3 = pygame.Rect(0, self._gap, self._gap, self._screen_height-self._gap*2)
        r4 = pygame.Rect(self._gap, self._screen_height-self._gap, self._screen_width-self._gap*2, self._gap)
        pygame.draw.rect(self._screen, pygame.Color(0, 100, 100), r)
        pygame.draw.rect(self._screen, pygame.Color(0, 100, 100), r2)
        pygame.draw.rect(self._screen, pygame.Color(0, 100, 100), r3)
        pygame.draw.rect(self._screen, pygame.Color(0, 100, 100), r4) """

        for y in range(len(self._content)):
            line = self._content[y]
            for x in range(len(line)):
                char = line[x]
                background, foreground = self._content_color[y][x]
                surface = self._printer.render(char, True, foreground, background)
                screen_x = self._gap + x * self._char_width
                screen_y = self._gap + y * self._line_height
                self._screen.blit(surface, (screen_x, screen_y))

        pygame.display.update()

