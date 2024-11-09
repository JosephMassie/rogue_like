#! ./.venv/bin/python3.12
import pygame, sys
from pygame.locals import *

from term import *
from world import *

def main():
    pygame.init();

    MAX_FPS = 60
    CLOCK = pygame.time.Clock()

    pygame.display.set_caption('Rogue Like')

    WIDTH = 40
    HEIGHT = 20
    terminal = Terminal(WIDTH, HEIGHT, 24)

    econ: TermContent = {
        "chars": [["g"]]
    }
    e1 = TermSprite(econ, 1, 1)
    e1.fillColor(pygame.Color(10, 0, 10), pygame.Color(0, 150, 150))

    pcon: TermContent = {
        "chars": [["@"]],
        "colors": [[(DEFAULT_BG_COLOR, pygame.Color(0, 150, 0))]]
    }
    player = TermSprite(pcon, 2, 2)

    levelOne = World("./assets/level_test.txt", terminal)

    timePassed = 0

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        
        pressed_keys = pygame.key.get_pressed()
        if timePassed >= 50:
            timePassed = 0
            if pressed_keys[K_UP]:
                player.y -= 1
            if pressed_keys[K_DOWN]:
                player.y += 1
            if pressed_keys[K_LEFT]:
                player.x -= 1
            if pressed_keys[K_RIGHT]:
                player.x += 1
            if pressed_keys[K_w]:
                levelOne.move_camera(0, -1)
            if pressed_keys[K_a]:
                levelOne.move_camera(-1, 0)
            if pressed_keys[K_s]:
                levelOne.move_camera(0, 1)
            if pressed_keys[K_d]:
                levelOne.move_camera(1, 0)
        
        #clamp player
        """ if player.x < 0:
            player.x = 0
        if player.x >= WIDTH:
            player.x = WIDTH - 1
        if player.y < 0:
            player.y = 0
        if player.y >= HEIGHT:
            player.y = HEIGHT - 1 """

        terminal.clear_buffer()
        levelOne.render()
        ecoords = levelOne.world_coord_to_screen_cord(e1.x, e1.y)
        terminal.draw_element(e1.content, *ecoords)
        pcoords = levelOne.world_coord_to_screen_cord(player.x, player.y)
        terminal.draw_element(player.content, *pcoords)
        terminal.update()

        timePassed += CLOCK.tick(MAX_FPS)

if __name__ == "__main__":
    main()
