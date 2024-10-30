import pygame, sys
from pygame.locals import *

from functools import reduce

type TermContent = list[list[str]]

class TermSprite():
    def __init__(self, content: TermContent, x: int, y: int) -> None:
        self.content = content
        self.x = x
        self.y = y

class Terminal():
    # takes in a width and length in character counts
    # creates a pygame screen based on the font_size and
    # those width and height values
    def __init__(
            self,
            width: int,
            height: int,
            font_size: int,
            background_color: pygame.Color = pygame.Color(50, 50, 50),
            gap: int = 10,
            default_color: pygame.Color = pygame.Color(255, 255, 255)
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
        # preform a quick render to get screen width
        surf = self._printer.render("".join(self._content[0]), True, self._default_color, self._bg_color)
        self._screen_width = surf.get_rect().width + gap * 2
        self._screen_height = height * self._line_height + gap * 2
        print(f"creating a terminal display of [{self._screen_width},{self._screen_height}]")
        self._screen = pygame.display.set_mode((self._screen_width, self._screen_height))
    
    def _get_element_width(self, elem: TermContent) -> int:
        greatest_width = 0
        for row in elem:
            width = len("".join(row))
            if width > greatest_width:
                greatest_width = width
        return greatest_width
    
    def _reduce_element_to_single_chars(self, elem: TermContent) -> TermContent:
        n_elem = elem.copy()
        for i in range(len(elem)):
            old_row = elem[i]
            row = []
            for piece in old_row:
                row += list(piece)
            n_elem[i] = row
        return n_elem
        

    def draw_element(self, elem: TermContent, x: int, y: int) -> None:
        if x < 0 or x >= self._width or y < 0 or y >= self._height:
            raise ValueError("can't draw element out of range, invalid coords")
        height = len(elem)
        width = self._get_element_width(elem)
        if x + width - 1 >= self._width or y + height - 1 >= self._height:
            raise ValueError("can't draw element out of range, too big")
        
        n_elem = self._reduce_element_to_single_chars(elem)
        for yy in range(height):
            for xx in range(width):
                self._content[y + yy][x + xx] = n_elem[yy][xx]
    
    def draw_term_sprite(self, spr: TermSprite) -> None:
        self.draw_element(spr.content, spr.x, spr.y)
    
    def clear_buffer(self) -> None:
        self._content = [["." for _ in range(self._width)] for _ in range(self._height)]

    # clear screen and render newly provided content
    def update(self) -> None:
        self._screen.fill(self._bg_color)
        
        r = pygame.Rect(self._screen_width-self._gap, self._gap, self._gap, self._screen_height - self._gap*2)
        r2 = pygame.Rect(self._gap, 0, self._screen_width-self._gap*2, self._gap)
        r3 = pygame.Rect(0, self._gap, self._gap, self._screen_height-self._gap*2)
        r4 = pygame.Rect(self._gap, self._screen_height-self._gap, self._screen_width-self._gap*2, self._gap)
        
        pygame.draw.rect(self._screen, pygame.Color(0, 100, 100), r)
        pygame.draw.rect(self._screen, pygame.Color(0, 100, 100), r2)
        pygame.draw.rect(self._screen, pygame.Color(0, 100, 100), r3)
        pygame.draw.rect(self._screen, pygame.Color(0, 100, 100), r4)

        for i in range(len(self._content)):
            line = "".join(self._content[i])
            surface = self._printer.render(line, True, self._default_color)
            x = self._gap
            y = self._gap + i * self._line_height
            self._screen.blit(surface, (x, y))

        pygame.display.update()

