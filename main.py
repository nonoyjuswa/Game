import pygame

pygame.init()

window_width, window_height = 1280, 720
display_screen = pygame.display.set_mode((windoow_width, window_height))
running = True

while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False

  display.fill('black')

pygame.quit()
