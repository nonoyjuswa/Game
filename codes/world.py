import pygame
from constants import *
from player import Player
from enemy import Enemy
from random import randint

class Obstacle:
    def __init__(self):
        self.rects = self.create_obstacles(NUMBER_OF_OBSTACLES)

    def create_obstacles(self, num):
        obstacles = []
        for _ in range(num):
            width, height = randint(30, 80), randint(30, 80)
            x = randint(0, WORLD_WIDTH - width)
            y = randint(0, WORLD_HEIGHT - height)
            obstacles.append(pygame.Rect(x, y, width, height))
        return obstacles

class World:
    def __init__(self):
        self.player = Player()
        self.enemies = [Enemy() for _ in range(ENEMY_NUMBER)]
        self.obstacles = Obstacle().rects
        self.world_surface = pygame.Surface((WORLD_WIDTH, WORLD_HEIGHT))
        self.camera = Camera()

    def draw(self, screen, cam_x, cam_y):
        # Draw the background color (outside the world)
        screen.fill('blue')  # Change 'blue' to your desired border color

        # Draw the world surface
        self.world_surface.fill('grey')

        # Draw player
        pygame.draw.rect(self.world_surface, 'green', self.player.rect)

        for enemy in self.enemies:
            pygame.draw.circle(self.world_surface, 'brown', enemy.rect.center, ENEMY_VISION_RADIUS, 1)
            pygame.draw.rect(self.world_surface, 'red', enemy.rect)

        for obstacle in self.obstacles:
            pygame.draw.rect(self.world_surface, 'white', obstacle)

        # Blit the world surface onto the screen
        screen.blit(self.world_surface, (-cam_x, -cam_y))

        # Draw health bar and icon on top of the world
        self.player.draw_health(screen)  # Draw health bar at the top left

    def update_enemies(self):
        for enemy in self.enemies:
            enemy.update_behavior(self.player, self.obstacles)

    def handle_player_movement(self, keys):
        self.player.move(keys, self.obstacles, self.enemies)


class Camera:
    @staticmethod
    def move(player_pos):
        cam_x = player_pos[0] - WINDOW_WIDTH // 2
        cam_y = player_pos[1] - WINDOW_HEIGHT // 2
        return cam_x, cam_y
