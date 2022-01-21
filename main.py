import pygame
import sys
from pygame.locals import *
import os
import pytmx
import random

FPS = 120
pygame.init()
all_sprites = pygame.sprite.Group()
obstacles_group = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
big_obstacles_group = pygame.sprite.Group()
diamond_group = pygame.sprite.Group()
size_sprite = {6: (90, 90), 15: (200, 200), 16: (200, 200), 17: (200, 200), 18: (200, 200), 20: (60, 60),
               24: (70, 160), 25: (70, 160), 27: (60, 60), 28: (60, 60), 29: (300, 300)}
sprite_name = {6: 'box'}


def load_image(name, color_key=None, convert=True, f='titles'):
    fullname = os.path.join(f'data/{f}', name)
    try:
        if convert:
            image = pygame.image.load(fullname).convert()
        else:
            image = pygame.image.load(fullname)
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


class StartWindow:
    def __init__(self):
        self.img = load_image("sound.png", convert=False, f='images')
        self.img = pygame.transform.scale(self.img, (40, 40))
        self.button = load_image("play_button.png", convert=False, f='images')
        self.button = pygame.transform.scale(self.button, (650, 350))
        self.button_sound = pygame.mixer.Sound('data/musics/button_sound.mp3')
        self.font = pygame.font.Font('data/fonts/font.otf', 90)

    def draw(self):
        global play_sound
        running = True
        while running:
            display.fill((255, 248, 231))
            screen.blit(pygame.transform.scale(display, screen.get_size()), (0, 0))
            screen.blit(self.img, (900, 20))
            screen.blit(self.button, (150, 150))
            text = self.font.render("Dinosaur Settlement", True, (171, 195, 87))
            screen.blit(text, (150, 100))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos
                    if (pos[0] > 880 and pos[0] < 980) and (pos[1] > 20 and pos[1] < 80) and play_sound:
                        self.img = load_image("no_sound.png", convert=False, f='images')
                        play_sound = False
                        self.img = pygame.transform.scale(self.img, (40, 40))
                        sound.stop()
                    elif (pos[0] > 880 and pos[0] < 980) and (pos[1] > 20 and pos[1] < 80) and not play_sound:
                        self.img = load_image("sound.png", convert=False, f='images')
                        play_sound = True
                        self.img = pygame.transform.scale(self.img, (40, 40))
                        sound.play()
                    elif (pos[0] > 215 and pos[0] < 720) and (pos[1] > 220 and pos[1] < 420):
                        self.button_sound.play()
                        running = False


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = load_image('din11.png', (255, 255, 255), f='images')
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (70, 70))
        self.mask = pygame.mask.from_surface(self.image)
        self.money_sound = pygame.mixer.Sound('data/musics/pick_up_money.mp3')
        self.rect.x = pos_x
        self.rect.y = pos_y

    def update(self):
        global count
        self.rect.x -= 1
        if pygame.key.get_pressed()[pygame.K_a] and not pygame.sprite.spritecollideany(self, obstacles_group) \
                and pygame.sprite.spritecollideany(
            self, tiles_group):
            if pygame.sprite.spritecollideany(self, big_obstacles_group) != None:
                if pygame.sprite.collide_mask(self, pygame.sprite.spritecollideany(self, big_obstacles_group)):
                    self.rect.x += 1
                else:
                    self.rect.x -= 1
            else:
                self.rect.x -= 1
        else:
            self.rect.x += 1
        self.rect.x += 1
        if pygame.key.get_pressed()[pygame.K_d] and not pygame.sprite.spritecollideany(self,
                                                                                       obstacles_group) \
                and pygame.sprite.spritecollideany(
            self, tiles_group):
            if pygame.sprite.spritecollideany(self, big_obstacles_group) != None:
                if pygame.sprite.collide_mask(self, pygame.sprite.spritecollideany(self, big_obstacles_group)):
                    self.rect.x -= 1
                else:
                    self.rect.x += 1
            else:
                self.rect.x += 1
        else:
            self.rect.x -= 1
        self.rect.y -= 1
        if pygame.key.get_pressed()[pygame.K_w] and not pygame.sprite.spritecollideany(self, obstacles_group) \
                and pygame.sprite.spritecollideany(self, tiles_group):
            if pygame.sprite.spritecollideany(self, big_obstacles_group) != None:
                if pygame.sprite.collide_mask(self, pygame.sprite.spritecollideany(self, big_obstacles_group)):
                    self.rect.y += 1
                else:
                    self.rect.y -= 1
            else:
                self.rect.y -= 1
        else:
            self.rect.y += 1
        self.rect.y += 1
        if pygame.key.get_pressed()[pygame.K_s] and not pygame.sprite.spritecollideany(self, obstacles_group) \
                and pygame.sprite.spritecollideany(self, tiles_group):
            if pygame.sprite.spritecollideany(self, big_obstacles_group) != None:
                if pygame.sprite.collide_mask(self, pygame.sprite.spritecollideany(self, big_obstacles_group)):
                    self.rect.y -= 1
                else:
                    self.rect.x += 1
            else:
                self.rect.y += 1
        else:
            self.rect.y -= 1
        if pygame.sprite.spritecollideany(self, diamond_group):
            self.money_sound.play()
            pygame.sprite.spritecollideany(self, diamond_group).kill()
            count += 10


class Dowload:
    def __init__(self):
        self.timer = pygame.time.Clock()
        self.im1 = load_image('dino1.png', f='images')
        self.im1 = pygame.transform.scale(self.im1, (70, 80))
        self.im2 = load_image('dino2.png', f='images')
        self.im2 = pygame.transform.scale(self.im2, (70, 80))
        self.im3 = load_image('dino3.png', f='images')
        self.im3 = pygame.transform.scale(self.im3, (70, 80))
        self.im4 = load_image('dino4.png', f='images')
        self.im4 = pygame.transform.scale(self.im4, (70, 80))

    def draw(self):
        count = 0
        font = pygame.font.Font('data/fonts/font.otf', 40)
        text_x = 380
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


class Diamond(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites, diamond_group)
        self.image = pygame.transform.scale(load_image('dimond.png', (255, 255, 255)), (35, 45))
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.rect.center = (pos_x, pos_y)
        # self.image = pygame.transform.scale(self.image, (50, 50))


class PolylineObj(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, name):
        super().__init__(all_sprites)
        self.image = load_image(f'{name}.png', (255, 255, 255))
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.rect.center = (pos_x, pos_y)
        self.life = 1000
        self.name = name
        self.x = pos_x
        self.y = pos_y

    def update(self):
        global count
        if self.life < 10:
            self.kill()
            if random.choice([True, False]):
                count += random.randint(2, 25)
        else:
            if pygame.key.get_pressed()[pygame.K_e] and pygame.sprite.spritecollideany(self, player_group):
                print(self.life)
                self.life -= 5
        if self.life != 1000:
            if self.life > 750:
                self.image = load_image(f'{self.name}_polyline.png', (255, 255, 255))
            if 750 > self.life > 500:
                self.image = load_image(f'{self.name}_medium_polyline.png', (255, 255, 255))
            if 500 > self.life > 250:
                self.image = load_image(f'{self.name}_more_polyline.png', (255, 255, 255))
            if 250 > self.life > 90:
                self.image = load_image(f'{self.name}_max_polyline.png', (255, 255, 255))


class Ostrov:
    def __init__(self):
        self.map_data = pytmx.load_pygame('data/maps/map.tmx')  # [[c for c in row] for row in f.read().split('\n')]

    def draw(self):
        # while True:
        display.fill((0, 0, 0))
        self.height = self.map_data.height
        self.width = self.map_data.width
        self.obstacles = []
        self.tiles = []
        for y in range(self.height):
            for x in range(self.width):
                if self.map_data.tiledgidmap[self.map_data.get_tile_gid(x, y, 0)] == 10 or \
                        self.map_data.tiledgidmap[
                            self.map_data.get_tile_gid(x, y, 0)] == 9 or \
                        self.map_data.tiledgidmap[
                            self.map_data.get_tile_gid(x, y, 0)] == 6:
                    Tile(self.map_data.get_tile_image(x, y, 0), 550 + x * 56 - y * 56, 120 + x * 32 + y * 32,
                         tiles_group)
                    self.tiles.append((x, y))
                if self.map_data.tiledgidmap[self.map_data.get_tile_gid(x, y, 0)] == 11 or \
                        self.map_data.tiledgidmap[
                            self.map_data.get_tile_gid(x, y, 0)] == 7:
                    Tile(self.map_data.get_tile_image(x, y, 0), 550 + x * 56 - y * 56, 120 + x * 32 + y * 32,
                         obstacles_group)
                    self.obstacles.append((x, y))
                if self.map_data.get_tile_image(x, y, 1) != None:
                    if self.map_data.tiledgidmap[self.map_data.get_tile_gid(x, y, 1)] != 6:
                        BigTile(self.map_data.get_tile_image(x, y, 1), 550 + x * 56 - y * 56, 120 + x * 32 + y * 32,
                                self.map_data.tiledgidmap[self.map_data.get_tile_gid(x, y, 1)],
                                big_obstacles_group)
                        self.obstacles.append((x, y))


        diaminds = random.randint(6, 50)
        for i in range(diaminds):
            x, y = random.randint(0, self.width), random.randint(0, self.height)
            while (x, y) in self.obstacles and (x, y) not in self.tiles:
                x, y = random.randint(0, self.width), random.randint(0, self.height)
            Diamond(550 + x * 56 - y * 56, 120 + x * 32 + y * 32)
            self.obstacles.append((x, y))
        ore = random.randint(6, 20)
        for i in range(ore):
            x, y = random.randint(0, self.width), random.randint(0, self.height // 2)
            while (x, y) in self.obstacles:
                x, y = random.randint(0, self.width), random.randint(0, self.height // 2)
            PolylineObj(550 + x * 56 - y * 56, 120 + x * 32 + y * 32, 'ore_deposits')
        screen.blit(pygame.transform.scale(display, screen.get_size()), (0, 0))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

    def more_dimond(self):
        diaminds = random.randint(6, 50)
        for i in range(diaminds):
            x, y = random.randint(0, self.width), random.randint(0, self.height)
            while (x, y) in self.obstacles and (x, y) not in self.tiles:
                x, y = random.randint(0, self.width), random.randint(0, self.height)
            Diamond(550 + x * 56 - y * 56, 120 + x * 32 + y * 32)


class BigTile(pygame.sprite.Sprite):
    def __init__(self, imge, pos_x, pos_y, num, *arg):
        super().__init__(all_sprites, *arg)
        sixe = size_sprite[num]
        self.image = pygame.transform.scale(imge, sixe)
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = (pos_x, pos_y)


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


def start_game(play_sound):
    if play_sound:
        play_sound = True
        img = load_image("sound.png", convert=False, f='images')
    else:
        play_sound = False
        img = load_image("no_sound.png", convert=False, f='images')
    player = Player(350, 1600)
    money_img = load_image("money_img.jpg", (255, 255, 255), f='images')
    money_img = pygame.transform.scale(money_img, (40, 40))
    img = pygame.transform.scale(img, (40, 40))
    running = True
    clock = pygame.time.Clock()
    camera = Camera()
    fon = pygame.image.load("data/images/fon_or.png")
    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if (pos[0] > 880 and pos[0] < 980) and (pos[1] > 20 and pos[1] < 80) and play_sound:
                    img = load_image("no_sound.png", convert=False, f='images')
                    play_sound = False
                    img = pygame.transform.scale(img, (40, 40))
                    sound.stop()
                elif (pos[0] > 880 and pos[0] < 980) and (pos[1] > 20 and pos[1] < 80) and not play_sound:
                    img = load_image("sound.png", convert=False, f='images')
                    play_sound = True
                    img = pygame.transform.scale(img, (40, 40))
                    sound.play()
        camera.update(player)
        for sprite in all_sprites:
            camera.apply(sprite)
        if len(diamond_group) <= 5:
            ostrov.more_dimond()
        screen.blit(fon, (0, 0))
        all_sprites.draw(screen)
        all_sprites.update()
        big_obstacles_group.draw(screen)
        player_group.update()
        screen.blit(img, (900, 20))
        screen.blit(money_img, (20, 20))
        pygame.display.flip()
        clock.tick(FPS)


pygame.display.set_caption('DinosaurSettlement')
sound = pygame.mixer.Sound('data/musics/Music.mp3')
sound.play()
play_sound = True
count = 0
icon = pygame.image.load('data/images/din.png')
pygame.display.set_icon(icon)
screen = pygame.display.set_mode((1000, 650), 0, 32)
display = pygame.Surface((300, 300))
startwin = StartWindow()
startwin.draw()
ostrov = Ostrov()
# dow = Dowload()
# dow.draw()
ostrov.draw()
start_game(play_sound)
