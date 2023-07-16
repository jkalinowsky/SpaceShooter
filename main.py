import os
import sys
import time
import random
import pygame

pygame.font.init()

width, height = 1280, 720
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('SpaceShooter')


# classes
class Ship:
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.laser = []
        self.cool_down_counter = 0

    def draw(self, window):
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y, 50, 50))


# load assets

def main():
    run = True
    fps = 60
    lives = 5
    main_font = pygame.font.SysFont('comicsans', 50)
    player_velocity = 5

    ship = Ship(300, 650)

    clock = pygame.time.Clock()

    def redraw_window():
        # screen.blit(background,(0,0))
        # draw lives
        lives_label = main_font.render(f'Lives: {lives}', 1, (255, 255, 255))
        screen.blit(lives_label, lives_label.get_rect(center=(width // 2, 50)))

        ship.draw(screen)

        pygame.display.update()

    while run:
        clock.tick(fps)
        redraw_window()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            ship.x -= player_velocity
        if keys[pygame.K_d]:
            ship.x += player_velocity
        if keys[pygame.K_w]:
            ship.y -= player_velocity
        if keys[pygame.K_s]:
            ship.y += player_velocity


main()
