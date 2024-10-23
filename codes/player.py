import pygame
from constants import *

class Player:
    def __init__(self):
        self.rect = pygame.Rect(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, PLAYER_SIZE, PLAYER_SIZE)

    def move(self, keys, obstacles):
        move_x, move_y = 0, 0

        if keys[pygame.K_a]:
            move_x -= PLAYER_SPEED
        if keys[pygame.K_d]:
            move_x += PLAYER_SPEED
        if keys[pygame.K_w]:
            move_y -= PLAYER_SPEED
        if keys[pygame.K_s]:
            move_y += PLAYER_SPEED

        # Normalize movement vector
        length = (move_x ** 2 + move_y ** 2) ** 0.5
        if length > 0:
            move_x /= length
            move_y /= length
            move_x *= PLAYER_SPEED
            move_y *= PLAYER_SPEED

        old_position = self.rect.topleft

        # Move player
        self.rect.x += move_x
        self.rect.y += move_y

        if self.check_collisions(obstacles):
            self.rect.topleft = old_position

        # Restrict player within world bounds
        self.rect.x = max(0, min(self.rect.x, WORLD_WIDTH - PLAYER_SIZE))
        self.rect.y = max(0, min(self.rect.y, WORLD_HEIGHT - PLAYER_SIZE))

    def check_collisions(self, obstacles):
        for obstacle in obstacles:
            if self.rect.colliderect(obstacle):
                return True
        return False
