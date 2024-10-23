import pygame
import sys
from player import Player
from enemy import Enemy
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
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Handle player movement
            keys = pygame.key.get_pressed()
            self.world.handle_player_movement(keys)

            # Update enemy behavior
            self.world.update_enemies()

            # Calculate camera movement
            cam_x, cam_y = self.world.camera.move(self.world.player.rect.topleft)

            # Draw everything
            self.world.draw(self.display_screen, cam_x, cam_y)

            # Update display
            pygame.display.flip()

            # Cap frame rate
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
