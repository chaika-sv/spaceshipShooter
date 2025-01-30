import pygame
from random import randint
from os.path import join

pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Space Shooter')
running = True

# surface
surf = pygame.Surface((100, 200))
surf.fill('orange')
x = 100

# import image
player_surf = pygame.image.load('../' + join('images', 'player.png')).convert_alpha()
star_surf = pygame.image.load('../' + join('images', 'star.png')).convert_alpha()

# generate stars
stars_number = 20
star_coordinates = [(randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)) for i in range(stars_number)]
print(star_coordinates)

while running:
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # draw the game
    display_surface.fill('black')

    for coord in star_coordinates:
        display_surface.blit(star_surf, coord)

    display_surface.blit(player_surf, (x, 150))


    x += 0.1
    pygame.display.update()

pygame.quit()