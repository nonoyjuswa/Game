import pygame
from constants import *


class Player:
    def __init__(self):
        self.rect = pygame.Rect(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, PLAYER_SIZE, PLAYER_SIZE)
        self.footprints = []  # diri gina butang ang mga footprint
        self.footprint_lifetime = 2000  # kung pila ka seconds madula ang footprint, miliseconds
        self.health = PLAYER_MAX_HEALTH  # max health sang player, initialize lang ni
        self.knockback_velocity = (0, 0)  # initialize ang knockback

    def move(self, keys, obstacles, enemies):  # movements....
        move_x, move_y = 0, 0

        # WSAD movement
        if keys[pygame.K_a]:
            move_x -= PLAYER_SPEED
        if keys[pygame.K_d]:
            move_x += PLAYER_SPEED
        if keys[pygame.K_w]:
            move_y -= PLAYER_SPEED
        if keys[pygame.K_s]:
            move_y += PLAYER_SPEED

        # na normalize ang pag incline nga movement para equal sa vertical kag horizntal
        length = (move_x ** 2 + move_y ** 2) ** 0.5
        if length > 0:
            move_x /= length
            move_y /= length
            move_x *= PLAYER_SPEED
            move_y *= PLAYER_SPEED

        # na check ang mga collisions sa enemy
        self.check_enemy_collisions(enemies)

        self.rect.x += move_x
        self.handle_collisions(obstacles, axis='x')

        # Move vertically and check for collisions
        self.rect.y += move_y
        self.handle_collisions(obstacles, axis='y')

            # diri nadi si knockback nga velocity ambot kung ano na hahahahaha, gin chatgpt ko nadi:
        if self.knockback_velocity != (0, 0):
            self.rect.x += self.knockback_velocity[0] * 0.5
            self.rect.y += self.knockback_velocity[1] * 0.5

            self.knockback_velocity = (
                self.knockback_velocity[0] * 0.9, self.knockback_velocity[1] * 0.9)
            if abs(self.knockback_velocity[0]) < 1 and abs(
                    self.knockback_velocity[1]) < 1:
                self.knockback_velocity = (0, 0)

        # footprint!! para sundan ni enemy, hindi mo lang galing makita
        if move_x != 0 or move_y != 0:
            footprint_position = (self.rect.centerx, self.rect.centery)
            self.footprints.append((footprint_position, pygame.time.get_ticks()))  # na append didto sa babaw nga list

        # gina remove ang footprint after certain time
        self.remove_old_footprints()

        # Para hindi mag lapaw si player sa sagwa ka world
        self.rect.x = max(0, min(self.rect.x, WORLD_WIDTH - PLAYER_SIZE))
        self.rect.y = max(0, min(self.rect.y, WORLD_HEIGHT - PLAYER_SIZE))

    # muni sya ang function sa pag remove
    def remove_old_footprints(self):
        current_time = pygame.time.get_ticks()
        self.footprints = [fp for fp in self.footprints if current_time - fp[1] < self.footprint_lifetime]

    # Health Icon or health bar
    def draw_health(self, screen):
        icon_size = 40
        health_bar_width = 100
        health_bar_height = 10
        icon_position = (10, 10)
        health_bar_position = (10, icon_position[1] + icon_size + 5)

        # Diri nadi butang ang icon sa sunod (tsura sang character)
        pygame.draw.rect(screen, 'black', (*icon_position, icon_size, icon_size))  # black danay

        # gina draw sa screen, maximum health ni sya (PULA)
        pygame.draw.rect(screen, 'red', (*health_bar_position, health_bar_width, health_bar_height))
        health_percentage = self.health / PLAYER_MAX_HEALTH
        # muni naman ang current health
        pygame.draw.rect(screen, 'green',
                         (*health_bar_position, health_bar_width * health_percentage, health_bar_height))  # Health bar

    # na check if may collisions sa mga obstacles
    def handle_collisions(self, obstacles, axis):
        for obstacle in obstacles:
            if not self.rect.colliderect(obstacle):
                continue  # Skip to the next obstacle if no collision

            if axis == 'x':  # Horizontal collision
                if self.rect.centerx < obstacle.centerx:  # Player is to the left
                    self.rect.right = obstacle.left  # Push player out to the left
                else:  # Player is to the right
                    self.rect.left = obstacle.right  # Push player out to the right
            elif axis == 'y':  # Vertical collision
                if self.rect.centery < obstacle.centery:  # Player is above
                    self.rect.bottom = obstacle.top  # Push player up
                else:  # Player is below
                    self.rect.top = obstacle.bottom  # Push player down

    # na check if may collisions sa enemy
    def check_enemy_collisions(self, enemies):
        for enemy in enemies:
            if self.rect.colliderect(enemy.rect):
                self.health -= 1  # Kung pila gina buhin mag collide or damage!

                # CHatgpt let's goo
                overlap_x = (self.rect.right - enemy.rect.left) if self.rect.centerx < enemy.rect.centerx else (
                        enemy.rect.right - self.rect.left)
                overlap_y = (self.rect.bottom - enemy.rect.top) if self.rect.centery < enemy.rect.centery else (
                        enemy.rect.bottom - self.rect.top)

                # diri nadi ang knockback, for example sa babaw nag collide kay enemy, ma knockback si player pa babaw
                if abs(overlap_x) < abs(overlap_y):
                    if self.rect.centerx < enemy.rect.centerx:
                        self.rect.right = enemy.rect.left
                        knockback_x = -8
                    else:
                        self.rect.left = enemy.rect.right
                        knockback_x = 8
                    knockback_y = 0
                else:
                    if self.rect.centery < enemy.rect.centery:
                        self.rect.bottom = enemy.rect.top
                        knockback_y = -8
                    else:
                        self.rect.top = enemy.rect.bottom
                        knockback_y = 8
                    knockback_x = 0

                self.rect.x += knockback_x
                self.rect.y += knockback_y

                self.knockback_velocity = (knockback_x, knockback_y)

                return True

        return False
