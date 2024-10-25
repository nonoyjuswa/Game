import pygame
from constants import *

class Player:
    def __init__(self):
        self.rect = pygame.Rect(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, PLAYER_SIZE, PLAYER_SIZE)
        self.footprints = []  # List to store footprints
        self.footprint_lifetime = 2000  # Lifetime of footprints in milliseconds
        self.health = PLAYER_MAX_HEALTH  # Initialize health to max health
        self.knockback_velocity = (0, 0) # Initialize knockback velocity

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

        # Store old position for reverting
        old_position = self.rect.topleft

        # Check for potential collision with enemies before moving
        collision_with_enemy = self.check_enemy_collisions(enemies)

        # Move player if no collision
        if not collision_with_enemy:
            self.rect.x += move_x  # Move player on the x-axis
            if not self.check_collisions(obstacles):  # Check obstacles after moving x
                self.rect.y += move_y  # Move player on the y-axis
                if self.check_collisions(obstacles):  # Check obstacles after moving y
                    self.rect.y -= move_y  # Revert y movement if collision detected
        else:
            self.rect.topleft = old_position  # Revert to old position if collision with enemy

        # Apply knockback
        if self.knockback_velocity != (0, 0):
            self.rect.x += self.knockback_velocity[0] * 0.5  # Slow down the knockback effect (adjust multiplier)
            self.rect.y += self.knockback_velocity[1] * 0.5

            # Gradually reduce knockback velocity to zero
            self.knockback_velocity = (
                self.knockback_velocity[0] * 0.9, self.knockback_velocity[1] * 0.9)  # Decay knockback over time
            if abs(self.knockback_velocity[0]) < 1 and abs(
                    self.knockback_velocity[1]) < 1:  # Stop knockback when negligible
                self.knockback_velocity = (0, 0)

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
                self.health -= 1  # Decrease health by 1 when colliding with an enemy

                # Calculate the overlap in both x and y directions
                overlap_x = (self.rect.right - enemy.rect.left) if self.rect.centerx < enemy.rect.centerx else (
                            enemy.rect.right - self.rect.left)
                overlap_y = (self.rect.bottom - enemy.rect.top) if self.rect.centery < enemy.rect.centery else (
                            enemy.rect.bottom - self.rect.top)

                # Determine the direction of the knockback based on overlap
                if abs(overlap_x) < abs(overlap_y):  # Horizontal collision
                    if self.rect.centerx < enemy.rect.centerx:  # Player is to the left of the enemy
                        self.rect.right = enemy.rect.left  # Move player to the left of the enemy
                        knockback_x = -20  # Knock back to the left
                    else:  # Player is to the right of the enemy
                        self.rect.left = enemy.rect.right  # Move player to the right of the enemy
                        knockback_x = 20  # Knock back to the right
                    knockback_y = 0  # No vertical knockback
                else:  # Vertical collision
                    if self.rect.centery < enemy.rect.centery:  # Player is above the enemy
                        self.rect.bottom = enemy.rect.top  # Move player above the enemy
                        knockback_y = -20  # Knock back up
                    else:  # Player is below the enemy
                        self.rect.top = enemy.rect.bottom  # Move player below the enemy
                        knockback_y = 20  # Knock back down
                    knockback_x = 0  # No horizontal knockback

                # Adjust player's position based on knockback
                self.rect.x += knockback_x
                self.rect.y += knockback_y

                # Store knockback velocity
                self.knockback_velocity = (knockback_x, knockback_y)

                return True  # Collision detected

        return False  # No collision detected

