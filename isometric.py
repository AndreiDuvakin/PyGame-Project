import pygame
import sys
from pygame.locals import *


class Ostrov:
    def __init__(self, *args):
        for i in args:
            if i == "ice":
                self.ice_img = pygame.image.load('imagine/ice.png').convert()
                self.ice_img.set_colorkey((255, 255, 255))
            if i == "water":
                self.water_img = pygame.image.load('imagine/water.png').convert()
                self.water_img.set_colorkey((255, 255, 255))
            if i == "box":
                self.box_img = pygame.image.load('imagine/box.png').convert()
                self.box_img.set_colorkey((255, 255, 255))
            if i == "kam":
                self.kam_img = pygame.image.load('imagine/kam.png').convert()
                self.kam_img.set_colorkey((255, 255, 255))
            if i == "snow":
                self.snow_img = pygame.image.load('imagine/snow.png').convert()
                self.snow_img.set_colorkey((255, 255, 255))
        f = open('map.txt')
        self.map_data = [[c for c in row] for row in f.read().split('\n')]
        f.close()

    def draw(self):
        while True:
            display.fill((0, 0, 0))

            for y, row in enumerate(self.map_data):
                for x, tile in enumerate(row):
                    if tile == "i":
                        display.blit(self.ice_img, (170 + x * 14 - y * 14, 120 + x * 8 + y * 8))
                    if tile == "b":
                        display.blit(self.box_img, (170 + x * 14 - y * 14, 120 + x * 8 + y * 8))
                    if tile == "s":
                        display.blit(self.snow_img, (170 + x * 14 - y * 14, 120 + x * 8 + y * 8))
                    if tile == "w":
                        display.blit(self.water_img, (170 + x * 14 - y * 14, 120 + x * 8 + y * 8))
                    if tile == "k":
                        display.blit(self.kam_img, (170 + x * 14 - y * 14, 120 + x * 8 + y * 8))
            screen.blit(pygame.transform.scale(display, screen.get_size()), (0, 0))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()


pygame.init()
pygame.display.set_caption('ostrov')
screen = pygame.display.set_mode((800, 800), 0, 32)
display = pygame.Surface((300, 300))
ostrov = Ostrov("ice", "box", "kam", "snow", "water")
ostrov.draw()


