#! ./.venv/bin/python3.12
import pygame, sys
from pygame.locals import *

from term import *

def main():
    pygame.init();

    MAX_FPS = 60
    CLOCK = pygame.time.Clock()

    pygame.display.set_caption('Rogue Like')

    WIDTH = 40
    HEIGHT = 20
    terminal = Terminal(WIDTH, HEIGHT, 24)
    e1 = TermSprite([["gyTl"]], 1, 1)

    player = TermSprite([["@"]], 0, 0)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_UP]:
            player.y -= 1
        if pressed_keys[K_DOWN]:
            player.y += 1
        if pressed_keys[K_LEFT]:
            player.x -= 1
        if pressed_keys[K_RIGHT]:
            player.x += 1
        
        #clamp player
        if player.x < 0:
            player.x = 0
        if player.x >= WIDTH:
            player.x = WIDTH - 1
        if player.y < 0:
            player.y = 0
        if player.y >= HEIGHT:
            player.y = HEIGHT - 1

        terminal.clear_buffer()
        terminal.draw_term_sprite(e1)
        terminal.draw_term_sprite(player)
        terminal.draw_element([['|'], ['|'], ['|'], ['|'], ['|'], ['|']], 19, 0)
        terminal.draw_element([["hello |"]], 10, 4)
        terminal.draw_element([["123456789"]], 0, 9)
        terminal.draw_element([["123456789"]], 0, 10)
        terminal.draw_element([["123456789"]], 0, 11)
        terminal.update()

        CLOCK.tick(MAX_FPS)

if __name__ == "__main__":
    main()
