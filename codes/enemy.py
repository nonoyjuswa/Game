import pygame
from random import randint
from constants import *
import math

# kung wala ni hindi sila mag work
def distance_between_points(point1, point2):
    """Calculate the distance between two points."""
    return math.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)

class Enemy:
    def __init__(self):
        self.rect = pygame.Rect(randint(100, WORLD_WIDTH - 100), randint(100, WORLD_HEIGHT - 100), ENEMY_SIZE, ENEMY_SIZE)
        self.original_pos = self.rect.topleft # iya zone
        self.chase = False # mag chase sa player
        self.last_seen_radar_pos = None # ang pula nga ga palibot sa enemy

    # enemy AI, with the help of your's truly... ChatGpt
    def update_behavior(self, player, obstacles):
        radar_position = player.footprints[-1][0] if player.footprints else None
        distance_to_radar = distance_between_points(radar_position, self.rect.center) if radar_position else float(
            'inf')

        if radar_position is not None and distance_to_radar <= ENEMY_VISION_RADIUS:
            self.chase = True
            self.last_seen_radar_pos = radar_position
            self.move_toward(radar_position, obstacles, player)
        else:
            if self.chase:
                if self.last_seen_radar_pos:
                    self.move_toward(self.last_seen_radar_pos, obstacles, player)
                    if distance_to_radar > ENEMY_VISION_RADIUS:
                        self.chase = False
                else:
                    self.chase = False

            self.follow_footprints(player, obstacles)

            if not self.chase:
                self.move_toward(self.original_pos, obstacles, player)

        # Check for collision with player and deduct health
        if self.rect.colliderect(player.rect):
            player.health -= 1  # Deduct health
            print("Player hit! Current health:", player.health)  # Optional: print current health

    # diri nadi gina follow ni enemy ang footsteps ni player
    def follow_footprints(self, player, obstacles):
        closest_footprint = None
        closest_distance = float('inf')

        for footprint in player.footprints:
            footprint_position = footprint[0]
            distance_to_footprint = distance_between_points(footprint_position, self.rect.center)

            if distance_to_footprint < closest_distance and distance_to_footprint <= ENEMY_VISION_RADIUS:
                closest_distance = distance_to_footprint
                closest_footprint = footprint_position

        if closest_footprint is not None:
            self.move_toward(closest_footprint, obstacles, player)

    # pag palapit ni enemy kay player kung gina chase
    def move_toward(self, target, obstacles, player):
        old_position = self.rect.topleft
        dx, dy = target[0] - self.rect.centerx, target[1] - self.rect.centery
        distance = math.hypot(dx, dy)

        if distance > 0:
            dx, dy = dx / distance, dy / distance
            self.rect.x += dx * ENEMY_SPEED
            self.rect.y += dy * ENEMY_SPEED

        # para hindi mag collide
        if self.check_collisions(obstacles) or self.rect.colliderect(player.rect):
            self.rect.topleft = old_position 
            self.try_alternate_path(dx, dy, obstacles, player)

    # para nadi sa mga obstacle kulang pani
    def try_alternate_path(self, dx, dy, obstacles, player):
        self.rect.y += dy * ENEMY_SPEED
        if self.check_collisions(obstacles) or self.rect.colliderect(player.rect):
            self.rect.y -= dy * ENEMY_SPEED 

        self.rect.x += dx * ENEMY_SPEED
        if self.check_collisions(obstacles) or self.rect.colliderect(player.rect):
            self.rect.x -= dx * ENEMY_SPEED 

    def check_collisions(self, obstacles):
        return any(self.rect.colliderect(obstacle) for obstacle in obstacles)
