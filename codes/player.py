import pygame
from constants import *

class Player:
    def __init__(self):
        self.rect = pygame.Rect(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, PLAYER_SIZE, PLAYER_SIZE)
        self.footprints = []  # List to store footprints
        self.footprint_lifetime = 2000  # Lifetime of footprints in milliseconds
        self.health = PLAYER_MAX_HEALTH  # Initialize health to max health

    def move(self, keys, obstacles, enemies):
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

        # Check collisions with obstacles
        if self.check_collisions(obstacles):
            self.rect.topleft = old_position

        # Check collisions with enemies
        self.check_enemy_collisions(enemies)

        # Add a footprint when the player moves
        if move_x != 0 or move_y != 0:
            footprint_position = (self.rect.centerx, self.rect.centery)
            self.footprints.append((footprint_position, pygame.time.get_ticks()))  # Store position and current time

        # Remove old footprints
        self.remove_old_footprints()

        # Restrict player within world bounds
        self.rect.x = max(0, min(self.rect.x, WORLD_WIDTH - PLAYER_SIZE))
        self.rect.y = max(0, min(self.rect.y, WORLD_HEIGHT - PLAYER_SIZE))

    def remove_old_footprints(self):
        current_time = pygame.time.get_ticks()
        self.footprints = [fp for fp in self.footprints if current_time - fp[1] < self.footprint_lifetime]

    def draw_footprints(self, screen):
        for footprint in self.footprints:
            position = footprint[0]
            pygame.draw.circle(screen, 'blue', (int(position[0]), int(position[1])), 5)  # Draw footprint circle

    def draw_health(self, screen):
        # Define positions and dimensions
        icon_size = 40  # Size of the icon
        health_bar_width = 100  # Width of the health bar
        health_bar_height = 10  # Height of the health bar
        icon_position = (10, 10)  # Position for the icon
        health_bar_position = (10, icon_position[1] + icon_size + 5)  # Position for the health bar

        # Draw the icon rectangle (placeholder for the future)
        pygame.draw.rect(screen, 'black', (*icon_position, icon_size, icon_size))  # Draw the icon rectangle

        # Draw the health bar background
        pygame.draw.rect(screen, 'red', (*health_bar_position, health_bar_width, health_bar_height))  # Background bar
        health_percentage = self.health / PLAYER_MAX_HEALTH  # Calculate health percentage
        # Draw the health bar
        pygame.draw.rect(screen, 'green', (*health_bar_position, health_bar_width * health_percentage, health_bar_height))  # Health bar

    def check_collisions(self, obstacles):
        for obstacle in obstacles:
            if self.rect.colliderect(obstacle):
                return True
        return False

    def check_enemy_collisions(self, enemies):
        for enemy in enemies:
            if self.rect.colliderect(enemy.rect):
                self.health -= 1  # Decrease health by 1
                print("Player hit! Current health:", self.health)
