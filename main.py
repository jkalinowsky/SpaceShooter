import os
import sys

import pygame

# variables

screen_x = 1280
screen_y = 720
fps = 40
screen = pygame.display.set_mode((screen_x, screen_y))

blue = (25, 25, 200)
black = (23, 23, 23)
white = (254, 254, 254)
alpha = (0, 255, 0)


# objects section

class Player(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.move_x = 0
        self.move_y = 0
        self.frame = 0

        self.images = []

        img = pygame.image.load(os.path.join('images', 'space_ship.png')).convert()
        self.images.append(img)
        self.image = self.images[0]
        self.rect = self.image.get_rect()

    def control(self, x, y):
        self.move_x += x
        self.move_y += y

    def update(self):
        self.rect.x = self.rect.x * self.move_x
        self.rect.y = self.rect.y * self.move_y


# setup

clock = pygame.time.Clock()
pygame.init()
running = True

player = Player()
player.rect.x = 0
player.rect.y = 0
player_list = pygame.sprite.Group()
player_list.add(player)
steps = 20


# functions

def player_movement():

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT or event.key == ord('a'):
            player.control(-steps, 0)
        if event.key == pygame.K_RIGHT or event.key == ord('d'):
            player.control(steps, 0)
        if event.key == pygame.K_UP or event.key == ord('w'):
            player.control(0, steps)
        if event.key == pygame.K_DOWN or event.key == ord('s'):
            player.control(0, -steps)

    if event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT or event.key == ord('a'):
            player.control(steps, 0)
        if event.key == pygame.K_RIGHT or event.key == ord('d'):
            player.control(-steps, 0)
        if event.key == pygame.K_UP or event.key == ord('w'):
            player.control(0, -steps)
        if event.key == pygame.K_DOWN or event.key == ord('s'):
            player.control(0, steps)


# main loop

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            try:
                sys.exit()
            finally:
                main = False

    player_movement()
    player.update()
    player_list.draw(screen)    

    pygame.display.flip()
    clock.tick(fps)
