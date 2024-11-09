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

    econ: TermContent = {
        "chars": [list("gyT1")]
    }
    e1 = TermSprite(econ, 1, 1)
    e1.fillColor(pygame.Color(10, 0, 10), pygame.Color(0, 150, 150))

    pcon: TermContent = {
        "chars": [["@"]],
        "colors": [[(terminal._bg_color, pygame.Color(0, 100, 0))]]
    }
    player = TermSprite(pcon, 0, 0)
    bg_test: TermContent = {
        "chars": [["#" for _ in range(WIDTH)] for _ in range(HEIGHT)]
    }
    bg_test_sprite = TermSprite(bg_test, 0, 0)
    bg_test_sprite.fillColor(pygame.Color(100, 0, 0), pygame.Color(150, 150, 150))

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
        terminal.draw_term_sprite(bg_test_sprite)
        terminal.draw_term_sprite(e1)
        terminal.draw_element({ "chars": [['|'], ['|'], ['|'], ['|'], ['|'], ['|']] }, 19, 0)
        terminal.draw_element({ "chars": [["hello |"]]}, 10, 4)
        terminal.draw_element({ "chars": [["123456789"]]}, 0, 9)
        terminal.draw_term_sprite(player)
        terminal.update()

        CLOCK.tick(MAX_FPS)

if __name__ == "__main__":
    main()
