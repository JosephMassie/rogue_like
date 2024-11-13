#! ./.venv/bin/python3.12
import pygame, sys
from pygame.locals import *

from term import *
from world import *
from utils.constants import *
from utils.input import Keyboard
from utils.int_vect import Int_Vector
from entities.player import Player

def main():
    pygame.init();

    CLOCK = pygame.time.Clock()

    pygame.display.set_caption('Rogue Like')

    terminal = Terminal(WIDTH, HEIGHT, FONT_SIZE)
    keyboard = Keyboard()

    levelOne = World("./assets/level_test.txt", terminal, keyboard)
    player = Player(levelOne.get_player_spawn(), terminal, levelOne, keyboard)

    e1 = TermSprite.fromSingleChar("g", color=(None, pygame.Color("#ce0808")), position=Int_Vector(10, 10))

    deltaT = 0
    while True:
        for event in pygame.event.get(exclude=[pygame.KEYDOWN, pygame.KEYUP]):
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        keyboard.update()

        if keyboard.pressed(pygame.K_ESCAPE):
            pygame.event.post(pygame.event.Event(QUIT))
        
        levelOne.update()
        player.update()

        # Start the Render cycle by clearing the char buffer
        terminal.clear_buffer()

        levelOne.render()

        ecoords = levelOne.world_coord_to_screen_cord(e1.pos)

        terminal.draw_content(e1.content, *ecoords.getCoords())

        player.render()

        # Complete the Render cycle by printing the char buffer to the screen
        terminal.render_buffer()

        deltaT = CLOCK.tick(MAX_FPS) / MS_IN_S

if __name__ == "__main__":
    main()
