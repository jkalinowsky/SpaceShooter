import os
import sys
import time
import random
import pygame

width, height = 1280, 720
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('SpaceShooter')


# load assets

def main():
    run = True
    fps = 60
    clock = pygame.time.Clock()

    def redraw_window():

        pygame.display.update()

    while run:
        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

main()
