import pygame
import sys
import math
from random import randint, choice

pygame.init()

window_width, window_height = 1280, 720
display_screen = pygame.display.set_mode((window_width, window_height))
running = True

world_width, world_height = 1560, 1440
world_surface = pygame.Surface((world_width, world_height))

player_x, player_y = window_width // 2, window_height // 2
player_speed = 5
player_size = 50
player_rect = pygame.Rect(player_x, player_y, player_size, player_size)

number_of_obstacles = 25

enemy_size = 50
enemy_speed = 2
enemy_original_pos = [randint(100, world_width - 100), randint(100, world_height -100)]
enemy_rect = pygame.Rect(enemy_original_pos[0], enemy_original_pos[1], enemy_size, enemy_size)
enemy_vision_radius = 300
patrol_width, patrol_height = 300, 300
patrol1, patrol2 = enemy_original_pos[0] - patrol_width // 2, enemy_original_pos[1] - patrol_height // 2
enemy_patrol_area = pygame.Rect(patrol1, patrol2, patrol_width, patrol_height)
enemy_chase = False
last_seen_player_pos = None

def create_obstacles(num):
    obstacles = []
    for i in range(num):
        width, height = randint(30,80), randint(30,80)

        x = randint(0, world_width - width)
        y = randint(0, world_height - height)

        obstacle = pygame.Rect(x, y, width, height)
        obstacles.append(obstacle)
    return obstacles

obstacles = create_obstacles(number_of_obstacles)

def check_collisions(player_rect, obstacles):
    for obstacle in obstacles:
        if player_rect.colliderect(obstacle):
            return True
    return False

def distance_between_enemy_and_player(point1, point2):
    return math.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)

def move_enemy_towards_player(enemy_rect, player_rect, speed = 3):
    direction_x = player_rect[0] - enemy_rect.centerx
    direction_y = player_rect[1] - enemy_rect.centery

    distance = math.sqrt(direction_x ** 2 + direction_y ** 2)

    if distance != 0:
        direction_x /= distance
        direction_y /= distance

    enemy_rect.x += int(direction_x * speed)
    enemy_rect.y += int(direction_y * speed)

def enemy_behavior(player_rect, enemy_rect):
    global enemy_chase, last_seen_player_pos

    distance_of_player = distance_between_enemy_and_player(player_rect, enemy_rect)

    if distance_of_player <= enemy_vision_radius:
        enemy_chase = True
        last_seen_player_pos = player_rect.center

        move_enemy_towards_player(enemy_rect, player_rect.center)
    elif enemy_chase and distance_of_player > enemy_vision_radius:
        if last_seen_player_pos:
            move_enemy_original_pos(enemy_rect, last_seen_player_pos)
            if distance_between_enemy_and_player(enemy_rect.center, last_seen_player_pos) < 10:
                enemy_chase = False
                last_seen_player_pos = None
    elif not enemy_chase:
        move_enemy_original_pos(enemy_rect, enemy_original_pos)
    # elif enemy_rect == enemy_patrol_area:
    #     random_enemy_direction(enemy_rect, enemy_patrol_area)

def move_enemy_original_pos(enemy_rect, target_point):
    dx, dy = target_point[0] - enemy_rect.centerx, target_point[1] - enemy_rect.centery
    distance = math.sqrt(dx ** 2 + dy ** 2)
    if distance > 0:
        dx, dy = dx / distance, dy / distance
        enemy_rect.x += dx * enemy_speed
        enemy_rect.y += dy * enemy_speed

def random_enemy_direction(enemy_rect, patrol_area):
    direction = choice(['up', 'down', 'left', 'right'])

    if direction == 'up' and enemy_rect.top > patrol_area.top:
        enemy_rect.y -= enemy_speed
    elif direction == 'down' and enemy_rect.bottom < patrol_area.bottom:
        enemy_rect.y += enemy_speed
    elif direction == 'left' and enemy_rect.left > patrol_area.left:
        enemy_rect.x -= enemy_speed
    elif direction == 'right' and enemy_rect.right < patrol_area.right:
        enemy_rect.x += enemy_speed

def camera_movement(player_pos):
    cam_x = player_pos[0] - window_width // 2
    cam_y = player_pos[1] - window_height // 2
    return cam_x, cam_y

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    display_screen.fill('black')

    old_position = player_rect.topleft

    keys = pygame.key.get_pressed()

    if keys[pygame.K_a]:
        player_rect.x -= player_speed
        if check_collisions(player_rect, obstacles):
            player_rect.x += player_speed
    elif keys[pygame.K_d]:
        player_rect.x += player_speed
        if check_collisions(player_rect, obstacles):
            player_rect.x -= player_speed
    elif keys[pygame.K_w]:
        player_rect.y -= player_speed
        if check_collisions(player_rect, obstacles):
            player_rect.y += player_speed
    elif keys[pygame.K_s]:
        player_rect.y += player_speed
        if check_collisions(player_rect, obstacles):
            player_rect.y -= player_speed

    player_rect.x = max(0, min(player_rect.x, world_width - player_size))
    player_rect.y = max(1, min(player_rect.y, world_height - player_size))

    enemy_behavior(player_rect, enemy_rect)

    cam_x, cam_y = camera_movement(player_rect.topleft)

    world_surface.fill('grey')

    pygame.draw.circle(world_surface, ' brown', enemy_rect.center, enemy_vision_radius, 1)

    pygame.draw.rect(world_surface, 'green', player_rect)

    pygame.draw.rect(world_surface, 'red', enemy_rect)

    for obstacle in obstacles:
        pygame.draw.rect(world_surface, 'white', obstacle)

    display_screen.blit(world_surface, (-cam_x, -cam_y))

    pygame.display.flip()

    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()