import pygame
import sys
from pygame.locals import *
import os

FPS = 60
pygame.init()
all_sprites = pygame.sprite.Group()
obstacles_group = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


def load_image(name, color_key=None):
    fullname = os.path.join('imagine', name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = load_image('din11.png', (255, 255, 255))
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect.x = pos_x
        self.rect.y = pos_y

    def update(self):
        self.rect.x -= 1
        if pygame.key.get_pressed()[pygame.K_LEFT] and not pygame.sprite.spritecollideany(self, obstacles_group) \
                and pygame.sprite.spritecollideany(
            self, tiles_group):
            self.rect.x -= 1
        else:
            self.rect.x += 1
        self.rect.x += 1
        if pygame.key.get_pressed()[pygame.K_RIGHT] and not pygame.sprite.spritecollideany(self,
                                                                                           obstacles_group) \
                and pygame.sprite.spritecollideany(
            self, tiles_group):
            self.rect.x += 1
        else:
            self.rect.x -= 1
        self.rect.y -= 1
        if pygame.key.get_pressed()[pygame.K_UP] and not pygame.sprite.spritecollideany(self, obstacles_group) \
                and pygame.sprite.spritecollideany(self, tiles_group):
            self.rect.y -= 1
        else:
            self.rect.y += 1
        self.rect.y += 1
        if pygame.key.get_pressed()[pygame.K_DOWN] and not pygame.sprite.spritecollideany(self,
                                                                                          obstacles_group) \
                and pygame.sprite.spritecollideany(
            self, tiles_group):
            self.rect.y += 1
        else:
            self.rect.y -= 1


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
        # while True:
        display.fill((0, 0, 0))
        for y, row in enumerate(self.map_data):
            for x, tile in enumerate(row):
                if tile == "i":
                    Tile(self.ice_img, 550 + x * 56 - y * 56, 120 + x * 32 + y * 32, obstacles_group)
                if tile == "b":
                    Tile(self.box_img, 550 + x * 56 - y * 56, 120 + x * 32 + y * 32, tiles_group)
                if tile == "s":
                    Tile(self.snow_img, 550 + x * 56 - y * 56, 120 + x * 32 + y * 32, tiles_group)
                if tile == "w":
                    Tile(self.water_img, 550 + x * 56 - y * 56, 120 + x * 32 + y * 32, obstacles_group)
                if tile == "k":
                    Tile(self.kam_img, 550 + x * 56 - y * 56, 120 + x * 32 + y * 32, tiles_group)
        screen.blit(pygame.transform.scale(display, screen.get_size()), (0, 0))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()


class Tile(pygame.sprite.Sprite):
    def __init__(self, imge, pos_x, pos_y, *arg):
        super().__init__(all_sprites, *arg)
        self.rect = imge.get_rect().move(pos_x, pos_y)
        self.image = pygame.transform.scale(imge, (100, 100))
        self.rect.center = (pos_x, pos_y)


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - 1000 // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - 650 // 2)


def start_game():
    player = Player(500, 325)
    running = True
    clock = pygame.time.Clock()
    camera = Camera()
    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        camera.update(player)
        for sprite in all_sprites:
            camera.apply(sprite)
        all_sprites.draw(screen)
        all_sprites.update()
        player_group.update()
        pygame.display.flip()
        clock.tick(FPS)


pygame.display.set_caption('DinosaurSettlement')
icon = pygame.image.load('imagine/din.png')
pygame.display.set_icon(icon)
screen = pygame.display.set_mode((1000, 650), 0, 32)
display = pygame.Surface((300, 300))
ostrov = Ostrov("ice", "box", "kam", "snow", "water")
# dow = Dowload()
# dow.draw()
ostrov.draw()
start_game()
