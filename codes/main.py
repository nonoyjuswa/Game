import pygame
import sys
from world import World
from constants import *

class Game:
    def __init__(self):
        pygame.init()
        self.display_screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.world = World()
        self.clock = pygame.time.Clock()
        self.running = True

    def run(self):
        while self.running:
            # ang button sang exit para mag exit
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # mga keyboard keys para sa movement
            keys = pygame.key.get_pressed()
            self.world.handle_player_movement(keys)

            # gina update ang enemy AI
            self.world.update_enemies()

            #camera movement or ang screen nga ga sunod sa player
            cam_x, cam_y = self.world.camera.move(self.world.player.rect.topleft)

            # na butang ang tanantanan
            self.world.draw(self.display_screen, cam_x, cam_y)

            # na update ang bilog nga world
            pygame.display.flip()

            # frame rate
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

# para sa pag run, ma run sya if ara sa main ang naopen
if __name__ == "__main__":
    game = Game()
    game.run()
