import pygame
import sys
from pygame.locals import *


class Dowload:
    def __init__(self):
        self.timer = pygame.time.Clock()
        self.im1 = pygame.image.load('imagine/dino1.png')
        self.im1.set_colorkey((255, 255, 255))
        self.im2 = pygame.image.load('imagine/dino2.png')
        self.im2.set_colorkey((255, 255, 255))
        self.im3 = pygame.image.load('imagine/dino3.png')
        self.im3.set_colorkey((255, 255, 255))
        self.im4 = pygame.image.load('imagine/dino4.png')
        self.im4.set_colorkey((255, 255, 255))

    def draw(self):
        count = 0
        font = pygame.font.Font(None, 40)
        text_x = 300
        text_y = 450

        for i in range(20):
            display.fill((255, 255, 255))
            if count == 0:
                display.blit(self.im1, (100, 100))
                text = font.render("loading", True, (171, 195, 87))
            elif count == 1:
                display.blit(self.im2, (100, 100))
                text = font.render("loading.", True, (171, 195, 87))
            elif count == 2:
                display.blit(self.im3, (100, 100))
                text = font.render("loading..", True, (171, 195, 87))
            elif count == 3:
                display.blit(self.im4, (100, 100))
                text = font.render("loading...", True, (171, 195, 87))
            screen.blit(pygame.transform.scale(display, screen.get_size()), (0, 0))
            screen.blit(text, (text_x, text_y))
            pygame.display.update()
            self.timer.tick(5)
            count = (count + 1) % 4

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
        f = open('map1.txt')
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
pygame.display.set_caption('DinosaurSettlement')
icon = pygame.image.load('imagine/din.png')
pygame.display.set_icon(icon)
screen = pygame.display.set_mode((800, 800), 0, 32)
display = pygame.Surface((300, 300))
ostrov = Ostrov("ice", "box", "kam", "snow", "water")
dow = Dowload()
dow.draw()
ostrov.draw()


