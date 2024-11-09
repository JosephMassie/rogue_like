import pygame, sys
from pygame.locals import *

from typing import TypedDict, Required, NotRequired
from functools import reduce

DEFAULT_BG_COLOR = pygame.Color(50, 50, 50)
DEFAULT_FG_COLOR = pygame.Color(255, 255, 255)
BLANK_CELL = " "

type TermCharBuff = list[list[str]]
type TermColorBuff = list[list[tuple[pygame.Color, pygame.Color]]]

class TermContent(TypedDict):
    chars: Required[TermCharBuff]
    colors: NotRequired[TermColorBuff]

def get_char_buff_width(buffer: TermCharBuff) -> int:
    greatest_width = 0
    for row in buffer:
        width = len("".join(row))
        if width > greatest_width:
            greatest_width = width
    return greatest_width

def get_clean_buffer_from_content(elem: TermContent) -> TermContent:
    chars = elem["chars"].copy()
    for i in range(len(elem["chars"])):
        old_row = elem["chars"][i]
        row = []
        for piece in old_row:
            row += list(piece)
        chars[i] = row
    return chars

class TermSprite():
    def __init__(self, content: TermContent, x: int, y: int) -> None:
        self.content = content
        self.x = x
        self.y = y
    
    def fillColor(self, color: pygame.Color, bgcolor: pygame.Color = DEFAULT_BG_COLOR):
        chars = self.content["chars"]
        height = len(chars)
        width = get_char_buff_width(self.content["chars"])
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

        self._line_height = self._printer.get_linesize()
        print(f"line size ? {self._line_height}")

        # set initial content to blank spaces
        self.clear_buffer()
        # preform a quick render to get screen width and individual character width
        surf = self._printer.render("".join(self._content[0]), True, self._default_color, self._bg_color)
        self._char_width = surf.get_rect().width / width
        self._screen_width = surf.get_rect().width + gap * 2
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
        

    def draw_element(self, elem: TermContent, x: int, y: int) -> None:
        if x < 0 or x >= self._width or y < 0 or y >= self._height:
            #print(f"can't draw element out of range, invalid coords [{x},{y}]")
            return
        
        chars = get_clean_buffer_from_content(elem)
        height = len(chars)
        width = get_char_buff_width(elem["chars"])

        for yy in range(height):
            if yy < self._height:
                for xx in range(len(chars[yy])):
                    if xx < self._width:
                        self._content[y + yy][x + xx] = chars[yy][xx]
        
        if "colors" in elem:
            colors = elem["colors"]
            for yy in range(len(colors)):
                if yy < self._height:
                    row = colors[yy]
                    for xx in range(len(row)):
                        if xx < self._width:
                            self._content_color[y + yy][x + xx] = row[xx]
        else:
            for yy in range(height):
                if yy < self._height:
                    for xx in range(width):
                        if xx < self._width:
                            self._content_color[y + yy][x + xx] = (self._bg_color, self._default_color)
    
    def draw_term_sprite(self, spr: TermSprite) -> None:
        self.draw_element(spr.content, spr.x, spr.y)

    # clear screen and render newly provided content
    def update(self) -> None:
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

