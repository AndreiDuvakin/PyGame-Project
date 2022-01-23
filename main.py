import pygame
import sys
from pygame.locals import *
import os
import pytmx
import random
import sqlite3

FPS = 130
pygame.init()
all_sprites = pygame.sprite.Group()
obstacles_group = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
big_obstacles_group = pygame.sprite.Group()
diamond_group = pygame.sprite.Group()
house_group = pygame.sprite.Group()
titles = [[9, 10, 31, 33], [7, 11, 32], [20, 24, 25, 27, 28, 29, 36], [6, 20], [15, 16, 17, 18]]
size_sprite = {6: (90, 90), 15: (200, 200), 16: (200, 200), 17: (200, 200), 18: (200, 200), 20: (60, 60),
               24: (70, 160), 25: (70, 160), 27: (60, 60), 28: (60, 60), 29: (300, 300)}
sprite_name = {6: 'box'}
house_count = 0
con = sqlite3.connect("data/base/data.sqlite")
cur = con.cursor()


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
        self.image = load_image('an_dino_1.png', (255, 255, 255), f='images')
        self.image = pygame.transform.scale(self.image, (70, int(70 * 0.8211)))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.money_sound = pygame.mixer.Sound('data/musics/pick_up_money.mp3')
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.stor = False

    def update(self):
        global money
        self.rect.x -= 1
        if pygame.key.get_pressed()[pygame.K_a] and not pygame.sprite.spritecollideany(self, obstacles_group) \
                and pygame.sprite.spritecollideany(
            self, tiles_group):
            if pygame.sprite.spritecollideany(self, big_obstacles_group) != None:
                if pygame.sprite.collide_mask(self, pygame.sprite.spritecollideany(self, big_obstacles_group)):
                    self.rect.x += 1
                else:
                    self.rect.x -= 1
                    if self.stor:
                        self.stor = False
                        self.image = pygame.transform.flip(self.image, True, False)
            else:
                self.rect.x -= 1
                if self.stor:
                    self.stor = False
                    self.image = pygame.transform.flip(self.image, True, False)
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
                    if not self.stor:
                        self.stor = True
                        self.image = pygame.transform.flip(self.image, True, False)
            else:
                self.rect.x += 1
                if not self.stor:
                    self.stor = True
                    self.image = pygame.transform.flip(self.image, True, False)
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
            money += 10


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
    def __init__(self, pos_x, pos_y, name, num=False):
        super().__init__(all_sprites, big_obstacles_group)
        self.image = load_image(f'{name}.png', (255, 255, 255))
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.rect.center = (pos_x, pos_y)
        self.num = num
        self.sound_money = pygame.mixer.Sound('data/musics/pick_up_money.mp3')
        if num:
            self.image = pygame.transform.scale(self.image, size_sprite[num])
            self.box_sound = pygame.mixer.Sound('data/musics/krack_box.mp3')
        else:
            self.rude_sound = pygame.mixer.Sound('data/musics/kirka_lomik.mp3')
        self.life = 1000
        self.name = name
        self.x = pos_x
        self.y = pos_y
        self.f = 0

    def update(self):
        global money
        if self.num and self.f == 1 and not (
                pygame.key.get_pressed()[pygame.K_e] and pygame.sprite.spritecollideany(self, player_group)):
            self.f = 0
            self.box_sound.stop()
        elif self.num is False and self.f == 2 and not (
                pygame.key.get_pressed()[pygame.K_e] and pygame.sprite.spritecollideany(self, player_group)):
            self.f = 0
            self.rude_sound.stop()
        if self.life < 10:
            if self.num:
                self.box_sound.stop()
            else:
                self.rude_sound.stop()
            money += 0 if random.choice([False, False, False, True]) else random.randint(5, 25)
            self.kill()
            self.sound_money.play()
        else:
            if pygame.key.get_pressed()[pygame.K_e] and pygame.sprite.spritecollideany(self, player_group):
                self.life -= 2 if self.num else 5
                if self.num and self.f == 0:
                    self.box_sound.play()
                    self.f = 1
                if self.num is False and self.f == 0:
                    self.rude_sound.play()
                    self.f = 2
        if self.life != 1000:
            if self.life > 750:
                self.image = load_image(f'{self.name}_polyline.png', (255, 255, 255))
                if self.num:
                    self.image = pygame.transform.scale(self.image, size_sprite[self.num])
            if 750 > self.life > 500:
                self.image = load_image(f'{self.name}_medium_polyline.png', (255, 255, 255))
                if self.num:
                    self.image = pygame.transform.scale(self.image, size_sprite[self.num])
            if 500 > self.life > 250:
                self.image = load_image(f'{self.name}_more_polyline.png', (255, 255, 255))
                if self.num:
                    self.image = pygame.transform.scale(self.image, size_sprite[self.num])
            if 250 > self.life > 90:
                self.image = load_image(f'{self.name}_max_polyline.png', (255, 255, 255))
                if self.num:
                    self.image = pygame.transform.scale(self.image, size_sprite[self.num])


class House(pygame.sprite.Sprite):
    def __init__(self, imge, pos_x, pos_y, num, levels):
        global house_count
        super().__init__(all_sprites, house_group, big_obstacles_group)
        sixe = size_sprite[num]
        self.image = pygame.transform.scale(imge, sixe)
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = (pos_x, pos_y)
        self.number = house_count
        try:
            con = sqlite3.connect("data/base/data.sqlite")
            cur = con.cursor()
            self.income = cur.execute(f"SELECT income from house WHERE"
                                      f" level = {str(levels)} and number = {self.number}").fetchall()[0][0]
            self.sold = True
        except IndexError:
            self.sold = False
            self.income = 0
        self.font = pygame.font.Font('data/fonts/Impact.ttf', 15)
        self.big_font = pygame.font.Font('data/fonts/Impact.ttf', 30)
        self.normal_font = pygame.font.Font('data/fonts/Impact.ttf', 18)
        self.text = self.font.render(
            f"Этот дом еще не куплен!",
            True, (255, 255, 255))
        self.text1 = self.font.render(
            f"Купите его и",
            True, (255, 255, 255))
        self.text2 = self.font.render(
            f"получайте доход",
            True, (255, 255, 255))
        self.text3 = self.font.render(
            f"1 монетку в секунду",
            True, (255, 255, 255))
        self.text4 = self.font.render(
            f"Этот дом ваш!",
            True, (255, 255, 255))
        self.text6 = self.font.render(
            f"Вы можете улучшить дом",
            True, (255, 255, 255))
        self.text7 = self.font.render(
            f"Вы не можете улучшить",
            True, (255, 0, 0))
        self.text8 = self.font.render(
            f"Недостаточно монет!",
            True, (255, 0, 0))
        self.text9 = self.normal_font.render(
            f"Дом полностью",
            True, (170, 238, 255))
        self.text10 = self.normal_font.render(
            f"Улучшен!",
            True, (170, 238, 255))
        self.board = load_image('fon_board_house.png', (0, 0, 0), f='images')
        self.money = pygame.transform.scale(load_image('money_img.jpg', (255, 255, 255), f='images'), (30, 30))
        self.but = pygame.transform.scale(load_image('buy_button.png', (0, 0, 0), f='images'), (185, 75))
        self.up_but = pygame.transform.scale(load_image('update_button.png', (0, 0, 0), f='images'), (185, 75))

    def update(self):
        global money
        global house_buy
        if self.sold:
            money += self.income / 60
        if pygame.sprite.spritecollideany(self, player_group):
            screen.blit(self.board, (self.rect.x - 170, self.rect.y + 40))
            if self.sold:
                screen.blit(self.text4, (self.rect.x - 160, self.rect.y + 60))
                screen.blit(self.font.render(
                    f"Ваш доход: {self.income}",
                    True, (255, 255, 255)), (self.rect.x - 160, self.rect.y + 75))
                if self.income < 10:
                    self.price_upgrate = (house_buy + self.income) * 1000 * 1.5
                    screen.blit(self.up_but,
                                (self.rect.x - 170, self.rect.y + 115))
                    if money - self.price_upgrate >= 0:
                        screen.blit(self.text6, (self.rect.x - 160, self.rect.y + 90))
                        screen.blit(self.big_font.render(
                            f"{str(int(self.price_upgrate))}",
                            True, (255, 255, 255)), (self.rect.x - 120, self.rect.y + 175))
                        screen.blit(
                            self.money,
                            (self.rect.x - 160, self.rect.y + 180))
                        button_cor = list(
                            set(list(
                                map(lambda x: x.pos if x.type == pygame.MOUSEBUTTONDOWN else False,
                                    pygame.event.get()))))
                        if button_cor != []:
                            if button_cor[0] != False:
                                x, y = button_cor[0]
                                if self.rect.x - 170 < x < self.rect.x + 15 \
                                        and self.rect.y + 115 < y < self.rect.y + 190:
                                    self.income += 1
                                    cur.execute(
                                        f"""UPDATE house SET income = {str(self.income)}
                                         WHERE level = {level} AND number = {self.number} """)
                                    con.commit()
                                    money -= self.price_upgrate
                    else:
                        screen.blit(self.text7, (self.rect.x - 160, self.rect.y + 90))
                        screen.blit(self.text8, (self.rect.x - 160, self.rect.y + 105))
                        screen.blit(self.big_font.render(
                            f"{str(int(self.price_upgrate))}",
                            True, (255, 0, 0)), (self.rect.x - 120, self.rect.y + 175))
                        screen.blit(
                            self.money,
                            (self.rect.x - 160, self.rect.y + 180))
                else:
                    screen.blit(self.text7, (self.rect.x - 160, self.rect.y + 90))
                    screen.blit(self.text9, (self.rect.x - 140, self.rect.y + 115))
                    screen.blit(self.text10, (self.rect.x - 125, self.rect.y + 140))
                    screen.blit(
                        self.money,
                        (self.rect.x - 100, self.rect.y + 180))
            else:
                self.price = int((house_buy + 1) * 1000 * 1.5)
                screen.blit(self.text, (self.rect.x - 160, self.rect.y + 60))
                screen.blit(self.text1, (self.rect.x - 120, self.rect.y + 75))
                screen.blit(self.text2, (self.rect.x - 135, self.rect.y + 90))
                screen.blit(self.text3, (self.rect.x - 145, self.rect.y + 105))
                if money - self.price >= 0:
                    screen.blit(self.big_font.render(
                        f"{str(self.price)}",
                        True, (234, 239, 91)), (self.rect.x - 120, self.rect.y + 175))
                    screen.blit(
                        self.money,
                        (self.rect.x - 160, self.rect.y + 180))
                    screen.blit(self.but,
                                (self.rect.x - 170, self.rect.y + 115))
                    button_cor = list(
                        set(list(
                            map(lambda x: x.pos if x.type == pygame.MOUSEBUTTONDOWN else False, pygame.event.get()))))
                    if button_cor != []:
                        if button_cor[0] != False:
                            x, y = button_cor[0]
                            if self.rect.x - 170 < x < self.rect.x + 15 and self.rect.y + 115 < y < self.rect.y + 190:
                                self.sold = True
                                self.income = 1
                                cur.execute(
                                    f"""INSERT INTO house(level, number, income)
                                 VALUES({str(level)}, {str(self.number)}, {str(self.income)})""")
                                con.commit()
                                money -= self.price
                                house_buy += 1

                screen.blit(pygame.transform.scale(load_image('buy_button.png', (0, 0, 0), f='images'), (185, 75)),
                            (self.rect.x - 170, self.rect.y + 115))
                if money - self.price < 0:
                    screen.blit(self.normal_font.render(
                        f"Недостаточно монет!",
                        True, (255, 0, 0)), (self.rect.x - 160, self.rect.y + 175))
                    screen.blit(self.font.render(
                        f"Необходимо {str(self.price)} монет",
                        True, (234, 239, 91)), (self.rect.x - 160, self.rect.y + 195))


class Ostrov:
    def __init__(self):
        global level
        if level == 1:
            self.map_data = pytmx.load_pygame('data/maps/map.tmx')  # [[c for c in row] for row in f.read().split('\n')]
        elif level == 2:
            self.map_data = pytmx.load_pygame('data/maps/map2.tmx')

    def draw(self):
        global house_count
        display.fill((0, 0, 0))
        self.height = self.map_data.height
        self.width = self.map_data.width
        self.obstacles = []
        self.tiles = []
        for y in range(self.height):
            for x in range(self.width):
                if self.map_data.tiledgidmap[self.map_data.get_tile_gid(x, y, 0)] in titles[0]:
                    Tile(self.map_data.get_tile_image(x, y, 0), 550 + x * 56 - y * 56, 120 + x * 32 + y * 32,
                         tiles_group)
                    self.tiles.append((x, y))
                if self.map_data.tiledgidmap[self.map_data.get_tile_gid(x, y, 0)] in titles[1]:
                    Tile(self.map_data.get_tile_image(x, y, 0), 550 + x * 56 - y * 56, 120 + x * 32 + y * 32,
                         obstacles_group)
                    self.obstacles.append((x, y))
                if self.map_data.get_tile_image(x, y, 1) != None:
                    if self.map_data.tiledgidmap[self.map_data.get_tile_gid(x, y, 1)] in titles[2]:
                        BigTile(self.map_data.get_tile_image(x, y, 1), 550 + x * 56 - y * 56, 120 + x * 32 + y * 32,
                                self.map_data.tiledgidmap[self.map_data.get_tile_gid(x, y, 1)],
                                big_obstacles_group)
                        self.obstacles.append((x, y))
                    elif self.map_data.tiledgidmap[self.map_data.get_tile_gid(x, y, 1)] in titles[3]:
                        PolylineObj(550 + x * 56 - y * 56, 120 + x * 32 + y * 32, 'box_title',
                                    self.map_data.tiledgidmap[self.map_data.get_tile_gid(x, y, 1)])
                    elif self.map_data.tiledgidmap[self.map_data.get_tile_gid(x, y, 1)] in titles[4]:
                        House(self.map_data.get_tile_image(x, y, 1), 550 + x * 56 - y * 56, 120 + x * 32 + y * 32,
                              self.map_data.tiledgidmap[self.map_data.get_tile_gid(x, y, 1)], level)
                        house_count += 1

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
            p = PolylineObj(550 + x * 56 - y * 56, 120 + x * 32 + y * 32, 'ore_deposits')
            if not pygame.sprite.spritecollideany(p, tiles_group):
                p.kill()
                ore += 1
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


class Instruction:
    def __init__(self):
        self.click_sound = pygame.mixer.Sound('data/musics/button_sound.mp3')
        self.image_strel = pygame.transform.scale(load_image("strelochka.png", (0, 0, 0), f='images'), (70, 70))
        self.font = pygame.font.Font('data/fonts/font.otf', 70)
        self.text = self.font.render("Instruction", True, (171, 195, 87))
        self.font2 = pygame.font.Font('data/fonts/dop_font.otf', 25)
        self.text_coord = 50
        self.count = 0

    def running(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        if self.count == 1:
                            self.click_sound.play()
                            self.instruction2()
                            running = False
                        elif self.count == 2:
                            self.click_sound.play()
                            running = False

    def instruction1(self):
        self.count = 1
        display.fill((255, 248, 231))
        screen.blit(pygame.transform.scale(display, screen.get_size()), (0, 0))

        image_din = pygame.transform.scale(load_image("dop_din.png", (255, 255, 255), f='images'), (110, 100))
        image_cat = pygame.transform.scale(load_image("dop_cat.png", (255, 255, 255), f='images'), (130, 120))

        intro_text = ["Добро пожаловать в поселение динозавров :з",
                      "Игра посвящается преподавателю, который всегда готов был нам помочь и научить нас...",
                      "",
                      "Для успешной игры рекомендуем вам изучить правила игры и основные положения"]
        opis_text = ["Главный персонаж, динозаврик, которым управлять будете вы ^-^",
                     "Еще один главный персонаж, милый котик, который будет давать задания ^-^"]

        screen.blit(self.text, (320, 4))
        screen.blit(image_din, (15, 230))
        screen.blit(image_cat, (15, 350))
        screen.blit(self.image_strel, (900, 550))
        texts = [intro_text, opis_text]
        for i in texts:
            for line in i:
                string_rendered = self.font2.render(line, True, pygame.Color('black'))
                intro_rect = string_rendered.get_rect()
                if i == intro_text:
                    intro_rect.x = 10
                    self.text_coord += 10
                else:
                    intro_rect.x = 150
                    self.text_coord += 100
                intro_rect.top = self.text_coord
                self.text_coord += intro_rect.height
                screen.blit(string_rendered, intro_rect)
                pygame.display.update()
            self.text_coord += 0
        self.running()

    def instruction2(self):
        image_diam = pygame.transform.scale(load_image("dop_diamond.png", (255, 255, 255), f='images'), (90, 100))
        image_depos = pygame.transform.scale(load_image("dop_deposits.png", (255, 255, 255), f='images'), (90, 100))
        image_box = pygame.transform.scale(load_image("dop_box.png", (255, 255, 255), f='images'), (90, 100))
        self.count = 2
        display.fill((255, 248, 231))
        screen.blit(pygame.transform.scale(display, screen.get_size()), (0, 0))
        screen.blit(self.text, (320, 4))
        screen.blit(self.image_strel, (900, 550))
        screen.blit(image_diam, (15, 190))
        screen.blit(image_depos, (15, 320))
        screen.blit(image_box, (15, 450))
        pygame.display.update()
        opis_text = ["Цель этой игры - заработать как можно больше монеток, чтобы развиваться дальше",
                     "Сейчас вы спросите как же это сделать :з",
                     "Давайте посмотрим"]
        diamon_text = ["Это алмазик, собирая его вы будете получать 10 монеток за каждый",
                       "Чтобы взять алмазик, просто подойдите к нему"]
        depos_text = ["А это руда. Но ее не так просто собрать",
                      "Чтобы собрать руду, подойдите к ней и зажмите 'E' на английской раскладке",
                      "За руду вы можете не получить ничего или в диапозоне от 5 до 25 монеток"]
        box_text = ["Это коробка. С ней все то же самое что и с рудой"]
        texts = [opis_text, diamon_text, depos_text, box_text]
        self.text_coord = 50
        for i in texts:
            for line in i:
                string_rendered = self.font2.render(line, True, pygame.Color('black'))
                intro_rect = string_rendered.get_rect()
                if i == opis_text:
                    intro_rect.x = 10
                else:
                    intro_rect.x = 150
                self.text_coord += 10
                intro_rect.top = self.text_coord
                self.text_coord += intro_rect.height
                screen.blit(string_rendered, intro_rect)
                pygame.display.update()
            self.text_coord += 30
        self.running()

    def instruction3(self):
        pass


def read_base():
    con = sqlite3.connect("data/base/data.sqlite")
    cur = con.cursor()
    result = cur.execute("""SELECT * FROM main""").fetchall()
    if not result:
        level = 1
        money = 0
    else:
        level = int(result[-1][1])
        money = int(result[-1][2])
    return level, money


def insert_base(level, money):
    con = sqlite3.connect("data/base/data.sqlite")
    cur = con.cursor()
    cur.execute("""INSERT INTO main(level, money, progress, datatime, sessiontime, actions) VALUES(?, ?, 0, 0, 0, 0)""",
                (item_id := int(level), int(money),))
    con.commit()
    con.close()


def start_game(play_sound):
    if play_sound:
        play_sound = True
        img = load_image("sound.png", convert=False, f='images')
    else:
        play_sound = False
        img = load_image("no_sound.png", convert=False, f='images')
    player = Player(350, 1600)
    money_img = load_image("money_img.jpg", (255, 255, 255), f='images')
    money_img = pygame.transform.scale(money_img, (30, 30))
    money_fon = pygame.transform.scale(load_image("new_money_fon.png", (0, 0, 0), f='images'), (350, 50))
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
                insert_base(level, money)
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
        screen.blit(money_fon, (0, 0))
        font = pygame.font.Font('data/fonts/font.otf', 50)
        text = font.render(f"{str(int(money))}", True, (255, 255, 255))
        screen.blit(text, (66, 4))
        screen.blit(money_img, (30, 10))
        pygame.display.flip()
        clock.tick(FPS)


pygame.display.set_caption('DinosaurSettlement')
sound = pygame.mixer.Sound('data/musics/Music.mp3')
sound.play()
play_sound = True
icon = pygame.image.load('data/images/din.png')
pygame.display.set_icon(icon)
money = 0
screen = pygame.display.set_mode((1000, 650), 0, 32)
display = pygame.Surface((300, 300))
level, money = read_base()
house_buy = len(cur.execute(f'SELECT id from house WHERE level = \'{level}\'').fetchall())
startwin = StartWindow()
startwin.draw()
instruction = Instruction()
instruction.instruction1()
ostrov = Ostrov()
dow = Dowload()
dow.draw()
ostrov.draw()
start_game(play_sound)
