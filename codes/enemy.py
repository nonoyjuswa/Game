import pygame
from random import randint
from constants import *
import math

def distance_between_points(point1, point2):
    """Calculate the distance between two points."""
    return math.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)

class Enemy:
    def __init__(self):
        self.rect = pygame.Rect(randint(100, WORLD_WIDTH - 100), randint(100, WORLD_HEIGHT - 100), ENEMY_SIZE, ENEMY_SIZE)
        self.original_pos = self.rect.topleft
        self.chase = False
        self.last_seen_player_pos = None

    def update_behavior(self, player, obstacles):
        distance_to_player = distance_between_points(player.rect.center, self.rect.center)

        if distance_to_player <= ENEMY_VISION_RADIUS:
            self.chase = True
            self.last_seen_player_pos = player.rect.center
            self.move_toward(player.rect.center, obstacles)
        elif self.chase and distance_to_player > ENEMY_VISION_RADIUS:
            if self.last_seen_player_pos:
                self.move_toward(self.last_seen_player_pos, obstacles)
                if distance_between_points(self.rect.center, self.last_seen_player_pos) < 10:
                    self.chase = False
                    self.last_seen_player_pos = None
        else:
            self.move_toward(self.original_pos, obstacles)

    def move_toward(self, target, obstacles):
        old_position = self.rect.topleft
        dx, dy = target[0] - self.rect.centerx, target[1] - self.rect.centery
        distance = math.sqrt(dx ** 2 + dy ** 2)

        if distance > 0:
            dx, dy = dx / distance, dy / distance
            self.rect.x += dx * ENEMY_SPEED
            self.rect.y += dy * ENEMY_SPEED

        # Check collisions and reset position if blocked
        if self.check_collisions(obstacles):
            self.rect.topleft = old_position
            self.try_alternate_path(dx, dy, obstacles)

    def try_alternate_path(self, dx, dy, obstacles):
        # Try moving only on the y-axis first, then on the x-axis
        self.rect.y += dy * ENEMY_SPEED
        if self.check_collisions(obstacles):
            self.rect.y -= dy * ENEMY_SPEED

        self.rect.x += dx * ENEMY_SPEED
        if self.check_collisions(obstacles):
            self.rect.x -= dx * ENEMY_SPEED

    def check_collisions(self, obstacles):
        for obstacle in obstacles:
            if self.rect.colliderect(obstacle):
                return True
        return False
