import pygame
from random import randint, uniform
from os.path import join

from pygame.event import custom_type


class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load('../' + join('images', 'player.png')).convert_alpha()
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 300

        # cooldown
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 400

    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_shoot_time >= self.cooldown_duration:
                self.can_shoot = True


    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        # when move diagonally normalize() decrease player_direction to normalize speed
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * dt

        recent_keys = pygame.key.get_just_pressed()
        if recent_keys[pygame.K_SPACE] and self.can_shoot:
            Laser(laser_surf, self.rect.midtop, all_sprites)
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()

        self.laser_timer()

class Star(pygame.sprite.Sprite):
    def __init__(self, groups, surf):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = (randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)))

class Laser(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(midbottom = pos)
        self.speed = 400

    def update(self, dt):
        self.rect.centery -= self.speed * dt
        if self.rect.bottom < 0:
            self.kill()

class Meteor(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = pos)
        self.speed = randint(400, 500)
        self.time_to_destroy = 3000
        self.created_time = pygame.time.get_ticks()
        self.direction = pygame.math.Vector2(uniform(-0.5, 0.5), 1)

    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt
        if pygame.time.get_ticks() - self.created_time >= self.time_to_destroy:
            self.kill()



pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Space Shooter')
running = True
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()

# import and generate
star_surf = pygame.image.load('../' + join('images', 'star.png')).convert_alpha()
laser_surf = pygame.image.load('../' + join('images', 'laser.png')).convert_alpha()
meteor_surf = pygame.image.load('../' + join('images', 'meteor.png')).convert_alpha()

# sprites
for i in range(20):
    Star(all_sprites, star_surf)
player = Player(all_sprites)


# custom events -> meteor event
meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 500)



while running:

    # tick(x) where x - fps (frames per second)
    # delta time - the time it took your computer to render the current frame in millisecond
    # for example for tick(120): 1 / 120 ~ 0,0083 seconds = 8-9 millisecond
    # to make your game indepent from actual computer speed we need to multiply player speed by delta time
    delta_time = clock.tick() / 1000

    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == meteor_event:
            x, y = randint(0, WINDOW_WIDTH), randint(-200, -100)
            Meteor(meteor_surf, (x, y), all_sprites)


    # update
    all_sprites.update(delta_time)

    # draw the game
    display_surface.fill('black')
    all_sprites.draw(display_surface)

    pygame.display.update()

pygame.quit()