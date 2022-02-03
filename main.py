import pygame
import sys
from pygame.locals import *
import os
import pytmx
import random
import sqlite3
import time

FPS = 150
pygame.init()
all_sprites = pygame.sprite.Group()
obstacles_group = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
big_obstacles_group = pygame.sprite.Group()
diamond_group = pygame.sprite.Group()
house_group = pygame.sprite.Group()
ore_group = pygame.sprite.Group()
cat_group = pygame.sprite.Group()
titles = [[9, 10, 31, 33], [7, 11, 32], [47, 46, 45, 39, 36, 37, 35, 20, 24, 25, 27, 28, 29, 36, 34, 48, 43, 42],
          [6, 20],
          [15, 16, 17, 18]]
size_sprite = {47: (80, 80), 46: (70, 160), 45: (300, 300), 39: (70, 160), 37: (270, 250), 36: (250, 250),
               35: (200, 200), 6: (90, 90), 15: (200, 200),
               16: (200, 200), 17: (200, 200), 18: (200, 200), 20: (60, 60),
               24: (70, 160), 25: (70, 160), 27: (60, 60), 28: (60, 60), 29: (300, 300), 34: (90, 90), 48: (160, 200),
               42: (60, 100), 43: (60, 60)}
sprite_name = {6: 'box'}
house_count = 0
con = sqlite3.connect("data/base/data.sqlite")
cur = con.cursor()


def new_game():
    cur.execute('DELETE from house')
    cur.execute('DELETE from main')
    cur.execute(f'INSERT INTO main(level, money, sessiontime) VALUES({1}, {0}, {0})')
    cur.execute(f'UPDATE quests SET done = 0')
    con.commit()
    play()


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


class Board(pygame.sprite.Sprite):
    def __init__(self, image):
        global level
        super().__init__(all_sprites, obstacles_group, cat_group)
        if level == 1:
            pos_x, pos_y = 370, 1385
        elif level == 2:
            pos_x, pos_y = 370, 1385
        elif level == 3:
            pos_x, pos_y = -430, 2100
        self.menu = 1
        self.image = pygame.transform.scale(image, (60, 60))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = (pos_x, pos_y)
        self.mini_font = pygame.font.Font('data/fonts/Impact.ttf', 13)
        self.font = pygame.font.Font('data/fonts/Impact.ttf', 15)
        self.big_font = pygame.font.Font('data/fonts/Impact.ttf', 30)
        self.normal_font = pygame.font.Font('data/fonts/Impact.ttf', 18)
        self.button_sound = pygame.mixer.Sound('data/musics/button_sound.mp3')
        self.window = pygame.transform.scale(load_image('fon_board_house.png', (0, 0, 0), f='images'), (400, 400))
        self.but_1 = pygame.transform.scale(load_image('one_button.png', (0, 0, 0), f='images'), (50, 50))
        self.but_2 = pygame.transform.scale(load_image('two_button.png', (0, 0, 0), f='images'), (50, 50))
        self.but_3 = pygame.transform.scale(load_image('three_button.png', (0, 0, 0), f='images'), (50, 50))
        self.text = self.normal_font.render('Приветствуем тебя в Dinosaur Settlement!', True, (255, 255, 255))
        self.text2 = self.font.render('Мы рады, что ты решил(а) сыграть в нашу игру!', True, (255, 255, 255))
        self.text3 = self.font.render('Ты находишься на первом уровне, и для перхода', True, (255, 255, 255))
        self.text4 = self.font.render('нужно накопить 200 000 монеток или больше,', True, (255, 255, 255))
        self.text5 = self.font.render('но не переживай! Их совсем не трудно заработать!', True, (255, 255, 255))
        self.text6 = self.normal_font.render('Листай на следующие странички', True, (255, 255, 255))
        self.text7 = self.normal_font.render('Где я объясню как это сделать', True, (255, 255, 255))
        self.text8 = self.normal_font.render('Желаю приятной игры!', True, (255, 255, 255))
        self.text9 = self.big_font.render('Простейший зароботок', True, (255, 255, 255))
        self.text10 = self.font.render('Самый простой способ зароботка это собирание', True, (255, 255, 255))
        self.text11 = self.font.render('алмазиков и собирание руды, но они отличаются.', True, (255, 255, 255))
        self.text12 = self.font.render('За алмазики всегда дается 10 монеток, чтобы их', True, (255, 255, 255))
        self.text13 = self.font.render('добыть нужно просто пройти через них! А вот за', True, (255, 255, 255))
        self.text14 = self.font.render('руду можно получить больше монеток, а можно', True, (255, 255, 255))
        self.text15 = self.font.render('и не получить вовсе! Все зависит от удачи :з', True, (255, 255, 255))
        self.text16 = self.font.render('Алмазики и руда на разных уровнях различаются,', True, (255, 255, 255))
        self.text17 = self.font.render('Но не пугайтесь, их свойства одинаковы :D', True, (255, 255, 255))
        self.text18 = self.big_font.render('Домики и котик!', True, (255, 255, 255))
        self.text19 = self.font.render('Домики! Их можно покупать и они будут приносить', True, (255, 255, 255))
        self.text20 = self.font.render('ежесекундный доход! Их можно улучшать и', True, (255, 255, 255))
        self.text21 = self.font.render('увеличивать доход от них!', True, (255, 255, 255))
        self.text22 = self.font.render('Котики! Все любят котиков! У нас тоже есть свой,', True, (255, 255, 255))
        self.text23 = self.font.render('он строгий но милый, гавкающий, но добрый и', True, (255, 255, 255))
        self.text24 = self.font.render('вредный, но щедрый и жезнерадостный! А еще', True, (255, 255, 255))
        self.text25 = self.font.render('он дает задания! За выполенние, которых он', True, (255, 255, 255))
        self.text26 = self.font.render('щедро награждает монетками! Именно выполняя', True, (255, 255, 255))
        self.text27 = self.font.render('задания ты накопишь нужную сумму!', True, (255, 255, 255))
        self.text28 = self.normal_font.render('Приветствуем тебя на втором уровне!', True, (255, 255, 255))
        self.text29 = self.font.render('Мы рады, что ты смог пройти первый уровень!', True, (255, 255, 255))
        self.text30 = self.font.render('На втором уровне тебе необходимо набрать уже', True, (255, 255, 255))
        self.text31 = self.font.render('370 000 монеток, но не переживай, накпоить их', True, (255, 255, 255))
        self.text32 = self.font.render('также просто, как и на первом уровне!', True, (255, 255, 255))
        self.text33 = self.normal_font.render('Приветствуем тебя на третьем уровне!', True, (255, 255, 255))
        self.text34 = self.font.render('Мы рады, что ты смог пройти второй уровень!', True, (255, 255, 255))
        self.text35 = self.font.render('На третьем уровне тебе необходимо набрать', True, (255, 255, 255))
        self.text36 = self.font.render('750 000 монеток, не переживай, накпоить их', True, (255, 255, 255))
        self.text37 = self.font.render('также просто, как и на прошлвх уровнях!', True, (255, 255, 255))
        self.we = pygame.transform.scale(load_image('we.png', (255, 255, 255), f='images'), (60, 120))

    def update(self):
        if pygame.sprite.spritecollideany(self, player_group):
            button_cor = list(
                set(list(
                    map(lambda x: x.pos if x.type == pygame.MOUSEBUTTONDOWN else False,
                        pygame.event.get()))))
            if button_cor != []:
                if button_cor[0] != False:
                    x, y = button_cor[0]
                    if self.rect.x - 120 < x < self.rect.x - 70 and self.rect.y + 120 < y < self.rect.y + 160:
                        self.menu = 1
                        self.button_sound.play()
                    elif self.rect.x - 20 < x < self.rect.x + 30 and self.rect.y + 120 < y < self.rect.y + 160:
                        self.menu = 2
                        self.button_sound.play()
                    elif self.rect.x + 80 < x < self.rect.x + 130 and self.rect.y + 120 < y < self.rect.y + 160:
                        self.menu = 3
                        self.button_sound.play()
            if level == 1:
                if self.menu == 1:
                    screen.blit(self.window, (self.rect.x - 200, self.rect.y - 200))
                    screen.blit(self.but_1, (self.rect.x - 120, self.rect.y + 120))
                    screen.blit(self.but_2, (self.rect.x - 20, self.rect.y + 120))
                    screen.blit(self.but_3, (self.rect.x + 80, self.rect.y + 120))
                    screen.blit(self.text, (self.rect.x - 175, self.rect.y - 150))
                    screen.blit(self.text2, (self.rect.x - 175, self.rect.y - 125))
                    screen.blit(self.text3, (self.rect.x - 180, self.rect.y - 100))
                    screen.blit(self.text4, (self.rect.x - 180, self.rect.y - 75))
                    screen.blit(self.text5, (self.rect.x - 180, self.rect.y - 50))
                    screen.blit(self.text6, (self.rect.x - 180, self.rect.y - 20))
                    screen.blit(self.text7, (self.rect.x - 180, self.rect.y + 10))
                    screen.blit(self.text8, (self.rect.x - 180, self.rect.y + 40))
                    screen.blit(self.we, (self.rect.x + 95, self.rect.y - 20))
                elif self.menu == 2:
                    screen.blit(self.window, (self.rect.x - 200, self.rect.y - 200))
                    screen.blit(self.but_1, (self.rect.x - 120, self.rect.y + 120))
                    screen.blit(self.but_2, (self.rect.x - 20, self.rect.y + 120))
                    screen.blit(self.but_3, (self.rect.x + 80, self.rect.y + 120))
                    screen.blit(self.text9, (self.rect.x - 165, self.rect.y - 165))
                    screen.blit(self.text10, (self.rect.x - 175, self.rect.y - 125))
                    screen.blit(self.text11, (self.rect.x - 180, self.rect.y - 100))
                    screen.blit(self.text12, (self.rect.x - 180, self.rect.y - 75))
                    screen.blit(self.text13, (self.rect.x - 180, self.rect.y - 50))
                    screen.blit(self.text14, (self.rect.x - 180, self.rect.y - 25))
                    screen.blit(self.text15, (self.rect.x - 180, self.rect.y))
                    screen.blit(self.text16, (self.rect.x - 180, self.rect.y + 25))
                    screen.blit(self.text17, (self.rect.x - 180, self.rect.y + 50))
                elif self.menu == 3:
                    screen.blit(self.window, (self.rect.x - 200, self.rect.y - 200))
                    screen.blit(self.but_1, (self.rect.x - 120, self.rect.y + 120))
                    screen.blit(self.but_2, (self.rect.x - 20, self.rect.y + 120))
                    screen.blit(self.but_3, (self.rect.x + 80, self.rect.y + 120))
                    screen.blit(self.text18, (self.rect.x - 115, self.rect.y - 165))
                    screen.blit(self.text19, (self.rect.x - 175, self.rect.y - 125))
                    screen.blit(self.text20, (self.rect.x - 175, self.rect.y - 100))
                    screen.blit(self.text21, (self.rect.x - 175, self.rect.y - 75))
                    screen.blit(self.text22, (self.rect.x - 175, self.rect.y - 50))
                    screen.blit(self.text23, (self.rect.x - 175, self.rect.y - 25))
                    screen.blit(self.text24, (self.rect.x - 175, self.rect.y))
                    screen.blit(self.text25, (self.rect.x - 175, self.rect.y + 25))
                    screen.blit(self.text26, (self.rect.x - 175, self.rect.y + 50))
                    screen.blit(self.text27, (self.rect.x - 175, self.rect.y + 75))
            elif level == 2:
                if self.menu == 1:
                    screen.blit(self.window, (self.rect.x - 200, self.rect.y - 200))
                    screen.blit(self.but_1, (self.rect.x - 120, self.rect.y + 120))
                    screen.blit(self.but_2, (self.rect.x - 20, self.rect.y + 120))
                    screen.blit(self.but_3, (self.rect.x + 80, self.rect.y + 120))
                    screen.blit(self.text28, (self.rect.x - 175, self.rect.y - 150))
                    screen.blit(self.text29, (self.rect.x - 175, self.rect.y - 125))
                    screen.blit(self.text30, (self.rect.x - 180, self.rect.y - 100))
                    screen.blit(self.text31, (self.rect.x - 180, self.rect.y - 75))
                    screen.blit(self.text32, (self.rect.x - 180, self.rect.y - 50))
                    screen.blit(self.text6, (self.rect.x - 180, self.rect.y - 20))
                    screen.blit(self.text7, (self.rect.x - 180, self.rect.y + 10))
                    screen.blit(self.text8, (self.rect.x - 180, self.rect.y + 40))
                    screen.blit(self.we, (self.rect.x + 95, self.rect.y - 20))
                elif self.menu == 2:
                    screen.blit(self.window, (self.rect.x - 200, self.rect.y - 200))
                    screen.blit(self.but_1, (self.rect.x - 120, self.rect.y + 120))
                    screen.blit(self.but_2, (self.rect.x - 20, self.rect.y + 120))
                    screen.blit(self.but_3, (self.rect.x + 80, self.rect.y + 120))
                    screen.blit(self.text9, (self.rect.x - 165, self.rect.y - 165))
                    screen.blit(self.text10, (self.rect.x - 175, self.rect.y - 125))
                    screen.blit(self.text11, (self.rect.x - 180, self.rect.y - 100))
                    screen.blit(self.text12, (self.rect.x - 180, self.rect.y - 75))
                    screen.blit(self.text13, (self.rect.x - 180, self.rect.y - 50))
                    screen.blit(self.text14, (self.rect.x - 180, self.rect.y - 25))
                    screen.blit(self.text15, (self.rect.x - 180, self.rect.y))
                    screen.blit(self.text16, (self.rect.x - 180, self.rect.y + 25))
                    screen.blit(self.text17, (self.rect.x - 180, self.rect.y + 50))
                elif self.menu == 3:
                    screen.blit(self.window, (self.rect.x - 200, self.rect.y - 200))
                    screen.blit(self.but_1, (self.rect.x - 120, self.rect.y + 120))
                    screen.blit(self.but_2, (self.rect.x - 20, self.rect.y + 120))
                    screen.blit(self.but_3, (self.rect.x + 80, self.rect.y + 120))
                    screen.blit(self.text18, (self.rect.x - 115, self.rect.y - 165))
                    screen.blit(self.text19, (self.rect.x - 175, self.rect.y - 125))
                    screen.blit(self.text20, (self.rect.x - 175, self.rect.y - 100))
                    screen.blit(self.text21, (self.rect.x - 175, self.rect.y - 75))
                    screen.blit(self.text22, (self.rect.x - 175, self.rect.y - 50))
                    screen.blit(self.text23, (self.rect.x - 175, self.rect.y - 25))
                    screen.blit(self.text24, (self.rect.x - 175, self.rect.y))
                    screen.blit(self.text25, (self.rect.x - 175, self.rect.y + 25))
                    screen.blit(self.text26, (self.rect.x - 175, self.rect.y + 50))
                    screen.blit(self.text27, (self.rect.x - 175, self.rect.y + 75))
            elif level == 3:
                if self.menu == 1:
                    screen.blit(self.window, (self.rect.x - 200, self.rect.y - 200))
                    screen.blit(self.but_1, (self.rect.x - 120, self.rect.y + 120))
                    screen.blit(self.but_2, (self.rect.x - 20, self.rect.y + 120))
                    screen.blit(self.but_3, (self.rect.x + 80, self.rect.y + 120))
                    screen.blit(self.text33, (self.rect.x - 175, self.rect.y - 150))
                    screen.blit(self.text34, (self.rect.x - 175, self.rect.y - 125))
                    screen.blit(self.text35, (self.rect.x - 180, self.rect.y - 100))
                    screen.blit(self.text36, (self.rect.x - 180, self.rect.y - 75))
                    screen.blit(self.text37, (self.rect.x - 180, self.rect.y - 50))
                    screen.blit(self.text6, (self.rect.x - 180, self.rect.y - 20))
                    screen.blit(self.text7, (self.rect.x - 180, self.rect.y + 10))
                    screen.blit(self.text8, (self.rect.x - 180, self.rect.y + 40))
                    screen.blit(self.we, (self.rect.x + 95, self.rect.y - 20))
                elif self.menu == 2:
                    screen.blit(self.window, (self.rect.x - 200, self.rect.y - 200))
                    screen.blit(self.but_1, (self.rect.x - 120, self.rect.y + 120))
                    screen.blit(self.but_2, (self.rect.x - 20, self.rect.y + 120))
                    screen.blit(self.but_3, (self.rect.x + 80, self.rect.y + 120))
                    screen.blit(self.text9, (self.rect.x - 165, self.rect.y - 165))
                    screen.blit(self.text10, (self.rect.x - 175, self.rect.y - 125))
                    screen.blit(self.text11, (self.rect.x - 180, self.rect.y - 100))
                    screen.blit(self.text12, (self.rect.x - 180, self.rect.y - 75))
                    screen.blit(self.text13, (self.rect.x - 180, self.rect.y - 50))
                    screen.blit(self.text14, (self.rect.x - 180, self.rect.y - 25))
                    screen.blit(self.text15, (self.rect.x - 180, self.rect.y))
                    screen.blit(self.text16, (self.rect.x - 180, self.rect.y + 25))
                    screen.blit(self.text17, (self.rect.x - 180, self.rect.y + 50))
                elif self.menu == 3:
                    screen.blit(self.window, (self.rect.x - 200, self.rect.y - 200))
                    screen.blit(self.but_1, (self.rect.x - 120, self.rect.y + 120))
                    screen.blit(self.but_2, (self.rect.x - 20, self.rect.y + 120))
                    screen.blit(self.but_3, (self.rect.x + 80, self.rect.y + 120))
                    screen.blit(self.text18, (self.rect.x - 115, self.rect.y - 165))
                    screen.blit(self.text19, (self.rect.x - 175, self.rect.y - 125))
                    screen.blit(self.text20, (self.rect.x - 175, self.rect.y - 100))
                    screen.blit(self.text21, (self.rect.x - 175, self.rect.y - 75))
                    screen.blit(self.text22, (self.rect.x - 175, self.rect.y - 50))
                    screen.blit(self.text23, (self.rect.x - 175, self.rect.y - 25))
                    screen.blit(self.text24, (self.rect.x - 175, self.rect.y))
                    screen.blit(self.text25, (self.rect.x - 175, self.rect.y + 25))
                    screen.blit(self.text26, (self.rect.x - 175, self.rect.y + 50))
                    screen.blit(self.text27, (self.rect.x - 175, self.rect.y + 75))


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
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.button_sound.play()
                        running = False


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        if level == 1:
            self.image = load_image('ZgizsloiDtI.jpg.png', (255, 255, 255), f='images')
            self.image = pygame.transform.scale(self.image, (70, int(70 * 0.8211)))
        elif level == 2:
            self.image = load_image('an_dino4.png', (255, 255, 255), f='images')
            self.image = pygame.transform.scale(self.image, (70, int(70 * 0.98)))
        elif level == 3:
            self.image = load_image('an_dino5.png', (255, 255, 255), f='images')
            self.image = pygame.transform.scale(self.image, (70, int(70 * 0.8511)))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.money_sound = pygame.mixer.Sound('data/musics/pick_up_money.mp3')
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.stor = False

    def update(self):
        global money
        global cat
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
            cat.diamond += 1
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
        if level == 1:
            i = 'dimond.png'
        elif level == 2:
            i = 'dimond2.png'
        elif level == 3:
            i = 'dimond3.png'
        self.image = pygame.transform.scale(load_image(i, (255, 255, 255)), (35, 45))
        self.rect = self.image.get_rect()
        self.rect.center = (pos_x, pos_y)
        # self.image = pygame.transform.scale(self.image, (50, 50))


class Cat(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        global house_buy
        global house_count
        house_count = 0
        house_buy = house_buy = len(cur.execute(f'SELECT id from house WHERE level = \'{level}\'').fetchall())
        super().__init__(all_sprites, cat_group, big_obstacles_group)
        self.image = pygame.transform.scale(load_image('dop_cat1.png', (255, 255, 255), f='images'),
                                            (60, int(60 * 1.157)))
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.menu = pygame.transform.scale(load_image('fon_board_house.png', (0, 0, 0), f='images'), (400, 400))
        self.active_task = False
        self.button_sound = pygame.mixer.Sound('data/musics/button_sound.mp3')
        self.diamond = 0
        self.ore = 0
        self.box = 0
        self.step_foot = 0
        self.buy_house = house_buy
        self.mini_font = pygame.font.Font('data/fonts/Impact.ttf', 13)
        self.font = pygame.font.Font('data/fonts/Impact.ttf', 15)
        self.big_font = pygame.font.Font('data/fonts/Impact.ttf', 30)
        self.normal_font = pygame.font.Font('data/fonts/Impact.ttf', 18)
        self.text = self.normal_font.render('Здравствуйте! Как ваше ничего?', True, (255, 255, 255))
        self.text2 = self.big_font.render('Награда', True, (230, 237, 25))
        self.text1 = self.normal_font.render('У меня есть отличное задание для тебя!', True, (255, 255, 255))
        self.text3 = self.normal_font.render('Ну, что, абрикосина? Согласен?', True, (255, 255, 255))
        self.but = pygame.transform.scale(load_image('ex_button.png', (0, 0, 0), f='images'), (350, 140))
        self.but_complete = pygame.transform.scale(load_image('compl_button.png', (0, 0, 0), f='images'), (350, 140))
        self.update_house = sum([int(i[0]) - 1 for i in cur.execute(
            f'SELECT income from house WHERE level = \'{level}\' AND income > 1').fetchall()])
        self.count = 0
        self.type_obj = False
        self.obj = False
        self.text7 = self.normal_font.render('Злые вы! Нет новых заданий!', True, (255, 255, 255))
        self.text8 = self.normal_font.render('Переходи на следующий уровень', True, (255, 255, 255))
        self.text91 = self.normal_font.render('и приходи за новыми заданиями!', True, (255, 255, 255))
        self.text4 = self.normal_font.render('Гав! Где выполненные задания??', True, (255, 255, 255))
        self.text5 = self.normal_font.render('Ого! Вижу ты выполнил задание!', True, (255, 255, 255))
        self.text6 = self.normal_font.render('Сдавай его и получай награду!', True, (255, 255, 255))
        self.mini_cat = pygame.transform.scale(load_image('dop_cat1.png', (255, 255, 255), f='images'),
                                               (45, int(45 * 1.157)))
        self.mini_menu = pygame.transform.scale(load_image('fon_board_house.png', (0, 0, 0), f='images'), (205, 150))
        self.text9 = self.normal_font.render('Задание:', True, (255, 255, 255))
        self.text10 = self.normal_font.render('Прогресс:', True, (255, 255, 255))
        self.text11 = self.font.render('Задание выполнено!', True, (255, 255, 255))
        self.text12 = self.font.render('и получи награду', True, (255, 255, 255))
        self.text13 = self.font.render('Вернись', True, (255, 255, 255))

    def update(self):
        global money
        if not self.active_task:
            if pygame.sprite.spritecollideany(self, player_group):
                try:
                    screen.blit(self.menu, (self.rect.x + 50, self.rect.y - 100))
                    screen.blit(self.text, (self.rect.x + 85, self.rect.y - 75))
                    screen.blit(self.text1, (self.rect.x + 85, self.rect.y - 45))
                    self.texts, self.mon, self.obj, self.count, self.id = \
                        cur.execute(f"SELECT text, awarding, typeobject,"
                                    f" count, id from quests"
                                    f" WHERE level = {level} AND"
                                    f" done = 0").fetchall()[0]
                    screen.blit(self.normal_font.render(self.texts, True, (255, 255, 255)),
                                (self.rect.x + 85, self.rect.y - 10))
                    screen.blit(self.text2, (self.rect.x + 85, self.rect.y + 15))
                    screen.blit(self.big_font.render(str(self.mon), True,
                                                     (230, 237, 25)), (self.rect.x + 200, self.rect.y + 15))
                    screen.blit(self.text3, (self.rect.x + 90, self.rect.y + 55))
                    screen.blit(self.but, (self.rect.x + 80, self.rect.y + 110))
                    screen.blit(self.mini_cat, (self.rect.x + 360, self.rect.y + 230))
                    button_cor = list(
                        set(list(
                            map(lambda x: x.pos if x.type == pygame.MOUSEBUTTONDOWN else False,
                                pygame.event.get()))))
                    if button_cor != []:
                        if button_cor[0] != False:
                            x, y = button_cor[0]
                            if self.rect.x + 80 < x < self.rect.x + 430 and self.rect.y + 110 < y < self.rect.y + 250:
                                self.active_task = True
                                self.button_sound.play()
                                self.type_obj = False
                                self.diamond = 0
                                self.ore = 0
                                self.step_foot = 0
                except IndexError:
                    if pygame.sprite.spritecollideany(self, player_group):
                        screen.blit(self.menu, (self.rect.x + 50, self.rect.y - 100))
                        screen.blit(self.text, (self.rect.x + 85, self.rect.y - 75))
                        screen.blit(self.text7, (self.rect.x + 95, self.rect.y - 45))
                        screen.blit(self.text8, (self.rect.x + 95, self.rect.y - 20))
                        screen.blit(self.text91, (self.rect.x + 95, self.rect.y - 5))
                        screen.blit(pygame.transform.scale(self.image, (180, 180 * 1.157)),
                                    (self.rect.x + 150, self.rect.y + 70))
        else:
            if self.obj == 'кристалл':
                self.type_obj = self.diamond
            elif self.obj == 'коробка':
                self.type_obj = self.box
            elif self.obj == 'дом':
                self.type_obj = self.buy_house
            elif self.obj == 'домЛ':
                self.type_obj = self.update_house
            elif self.obj == 'руда':
                self.type_obj = self.ore
            screen.blit(self.mini_menu, (0, 50))
            screen.blit(self.text9, (9, 58))
            screen.blit(self.mini_font.render(self.texts, True, (255, 255, 255)),
                        (9, 80))
            screen.blit(self.text2, (9, 135))
            screen.blit(self.font.render(str(self.mon), True, (230, 237, 25)), (15, 170))
            if self.type_obj < self.count:
                screen.blit(self.text10, (9, 95))
                screen.blit(self.font.render(str(self.type_obj), True, (255, 255, 255)), (9, 115))
                if pygame.sprite.spritecollideany(self, player_group):
                    screen.blit(self.menu, (self.rect.x + 50, self.rect.y - 100))
                    screen.blit(pygame.transform.scale(self.image, (180, 180 * 1.157)),
                                (self.rect.x + 150, self.rect.y + 70))
                    screen.blit(self.text, (self.rect.x + 85, self.rect.y - 75))
                    screen.blit(self.text4, (self.rect.x + 90, self.rect.y - 45))
                    screen.blit(self.normal_font.render(str(self.texts), True, (255, 255, 255)),
                                (self.rect.x + 85, self.rect.y - 10))
                    screen.blit(self.text2, (self.rect.x + 85, self.rect.y + 15))
                    screen.blit(self.big_font.render(str(self.mon), True, (230, 237, 25)),
                                (self.rect.x + 200, self.rect.y + 15))
            else:
                screen.blit(self.text11, (9, 95))
                screen.blit(self.text13, (9, 110))
                screen.blit(self.text12, (9, 125))
                if pygame.sprite.spritecollideany(self, player_group):
                    screen.blit(self.menu, (self.rect.x + 50, self.rect.y - 100))
                    screen.blit(self.text, (self.rect.x + 85, self.rect.y - 75))
                    screen.blit(self.text5, (self.rect.x + 85, self.rect.y - 45))
                    screen.blit(self.text6, (self.rect.x + 85, self.rect.y))
                    screen.blit(self.text2, (self.rect.x + 85, self.rect.y + 35))
                    screen.blit(self.big_font.render(str(self.mon), True,
                                                     (230, 237, 25)), (self.rect.x + 200, self.rect.y + 35))
                    screen.blit(self.but, (self.rect.x + 80, self.rect.y + 110))
                    screen.blit(self.mini_cat, (self.rect.x + 360, self.rect.y + 230))
                    button_cor = list(
                        set(list(
                            map(lambda x: x.pos if x.type == pygame.MOUSEBUTTONDOWN else False,
                                pygame.event.get()))))
                    if button_cor != []:
                        if button_cor[0] != False:
                            x, y = button_cor[0]
                            if self.rect.x + 80 < x < self.rect.x + 430 and self.rect.y + 110 < y < self.rect.y + 250:
                                self.active_task = False
                                self.count = 0
                                self.button_sound.play()
                                self.type_obj = 0
                                self.obj = False
                                self.diamond = 0
                                self.ore = 0
                                self.box = 0
                                self.step_foot = 0
                                money += self.mon
                                cur.execute(f'UPDATE quests SET done = 1 WHERE id = {self.id}')
                                con.commit()


class PolylineObj(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, name, num=False):
        super().__init__(all_sprites, big_obstacles_group)
        self.image = load_image(f'{name}.png', (255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (pos_x, pos_y)
        self.num = num
        self.sound_money = pygame.mixer.Sound('data/musics/pick_up_money.mp3')
        if num:
            self.image = pygame.transform.scale(self.image, size_sprite[num])
            self.box_sound = pygame.mixer.Sound('data/musics/krack_box.mp3')
        else:
            self.rude_sound = pygame.mixer.Sound('data/musics/kirka_lomik.mp3')
            ore_group.add(self)
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
            if self.num:
                cat.box += 1
            else:
                cat.ore += 1

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
        self.button_sound = pygame.mixer.Sound('data/musics/button_sound.mp3')
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
        self.board = pygame.transform.scale(load_image('fon_board_house.png', (0, 0, 0), f='images'), (210, 180))
        self.money = pygame.transform.scale(load_image('money_img.jpg', (255, 255, 255), f='images'), (30, 30))
        self.but = pygame.transform.scale(load_image('buy_button.png', (0, 0, 0), f='images'), (185, 75))
        self.up_but = pygame.transform.scale(load_image('update_button.png', (0, 0, 0), f='images'), (185, 75))

    def update(self):
        global money
        global house_buy
        if self.sold:
            money += self.income / 60
        if pygame.sprite.spritecollideany(self, player_group):
            screen.blit(self.board, (self.rect.x - 190, self.rect.y + 40))
            if self.sold:
                screen.blit(self.text4, (self.rect.x - 175, self.rect.y + 60))
                screen.blit(self.font.render(
                    f"Ваш доход: {self.income}",
                    True, (255, 255, 255)), (self.rect.x - 175, self.rect.y + 75))
                if self.income < 10:
                    self.price_upgrate = self.income * 500
                    screen.blit(self.up_but,
                                (self.rect.x - 180, self.rect.y + 115))
                    if money - self.price_upgrate >= 0:
                        screen.blit(self.text6, (self.rect.x - 175, self.rect.y + 90))
                        screen.blit(self.big_font.render(
                            f"{str(int(self.price_upgrate))}",
                            True, (255, 255, 255)), (self.rect.x - 135, self.rect.y + 175))
                        screen.blit(
                            self.money,
                            (self.rect.x - 175, self.rect.y + 180))
                        button_cor = list(
                            set(list(
                                map(lambda x: x.pos if x.type == pygame.MOUSEBUTTONDOWN else False,
                                    pygame.event.get()))))
                        if button_cor != []:
                            if button_cor[0] != False:
                                x, y = button_cor[0]
                                if self.rect.x - 185 < x < self.rect.x \
                                        and self.rect.y + 115 < y < self.rect.y + 190:
                                    self.income += 1
                                    self.button_sound.play()
                                    cat.update_house += 1
                                    cur.execute(
                                        f"""UPDATE house SET income = {str(self.income)}
                                         WHERE level = {level} AND number = {self.number} """)
                                    con.commit()
                                    money -= self.price_upgrate
                    else:
                        screen.blit(self.text7, (self.rect.x - 175, self.rect.y + 90))
                        screen.blit(self.text8, (self.rect.x - 175, self.rect.y + 105))
                        screen.blit(self.big_font.render(
                            f"{str(int(self.price_upgrate))}",
                            True, (255, 0, 0)), (self.rect.x - 135, self.rect.y + 175))
                        screen.blit(
                            self.money,
                            (self.rect.x - 175, self.rect.y + 180))
                else:
                    screen.blit(self.text7, (self.rect.x - 175, self.rect.y + 90))
                    screen.blit(self.text9, (self.rect.x - 155, self.rect.y + 115))
                    screen.blit(self.text10, (self.rect.x - 140, self.rect.y + 140))
                    screen.blit(
                        self.money,
                        (self.rect.x - 115, self.rect.y + 180))
            else:
                self.price = int((house_buy + 1) * 1000 * 1.1)
                screen.blit(self.text, (self.rect.x - 175, self.rect.y + 60))
                screen.blit(self.text1, (self.rect.x - 135, self.rect.y + 75))
                screen.blit(self.text2, (self.rect.x - 150, self.rect.y + 90))
                screen.blit(self.text3, (self.rect.x - 160, self.rect.y + 105))
                if money - self.price >= 0:
                    screen.blit(self.big_font.render(
                        f"{str(self.price)}",
                        True, (234, 239, 91)), (self.rect.x - 135, self.rect.y + 175))
                    screen.blit(
                        self.money,
                        (self.rect.x - 175, self.rect.y + 180))
                    screen.blit(self.but,
                                (self.rect.x - 180, self.rect.y + 115))
                    button_cor = list(
                        set(list(
                            map(lambda x: x.pos if x.type == pygame.MOUSEBUTTONDOWN else False, pygame.event.get()))))
                    if button_cor != []:
                        if button_cor[0] != False:
                            x, y = button_cor[0]
                            if self.rect.x - 185 < x < self.rect.x and self.rect.y + 115 < y < self.rect.y + 190:
                                self.sold = True
                                self.income = 1
                                self.button_sound.play()
                                cur.execute(
                                    f"""INSERT INTO house(level, number, income)
                                 VALUES({str(level)}, {str(self.number)}, {str(self.income)})""")
                                con.commit()
                                money -= self.price
                                house_buy += 1
                                cat.buy_house += 1
                if money - self.price < 0:
                    screen.blit(self.normal_font.render(
                        f"Недостаточно монет!",
                        True, (255, 0, 0)), (self.rect.x - 175, self.rect.y + 175))
                    screen.blit(self.font.render(
                        f"Необходимо {str(self.price)} монет",
                        True, (234, 239, 91)), (self.rect.x - 175, self.rect.y + 195))


class Ostrov:
    def __init__(self):
        global level
        if level == 1:
            self.map_data = pytmx.load_pygame('data/maps/map.tmx')  # [[c for c in row] for row in f.read().split('\n')]
        elif level == 2:
            self.map_data = pytmx.load_pygame('data/maps/map2.tmx')
        elif level == 3:
            self.map_data = pytmx.load_pygame('data/maps/map3.tmx')
        self.all_object = []
        self.ore = 6
        self.diaminds = 6

    def draw(self):
        global house_count
        global camera
        display.fill((0, 0, 0))
        self.height = self.map_data.height
        self.width = self.map_data.width
        self.obstacles = []
        self.tiles = []
        for y in range(self.height):
            for x in range(self.width):
                if self.map_data.tiledgidmap[self.map_data.get_tile_gid(x, y, 0)] in titles[0]:
                    t = Tile(self.map_data.get_tile_image(x, y, 0), 550 + x * 56 - y * 56, 120 + x * 32 + y * 32,
                             tiles_group)
                    self.all_object.append(t)
                    self.tiles.append((x, y))
                if self.map_data.tiledgidmap[self.map_data.get_tile_gid(x, y, 0)] in titles[1]:
                    t = Tile(self.map_data.get_tile_image(x, y, 0), 550 + x * 56 - y * 56, 120 + x * 32 + y * 32,
                             obstacles_group)
                    self.all_object.append(t)
                    self.obstacles.append((x, y))
                if self.map_data.get_tile_image(x, y, 1) != None:
                    if self.map_data.tiledgidmap[self.map_data.get_tile_gid(x, y, 1)] in titles[2]:
                        t = BigTile(self.map_data.get_tile_image(x, y, 1), 550 + x * 56 - y * 56, 120 + x * 32 + y * 32,
                                    self.map_data.tiledgidmap[self.map_data.get_tile_gid(x, y, 1)],
                                    big_obstacles_group)
                        self.all_object.append(t)
                        self.obstacles.append((x, y))
                    elif self.map_data.tiledgidmap[self.map_data.get_tile_gid(x, y, 1)] in titles[3]:
                        t = PolylineObj(550 + x * 56 - y * 56, 120 + x * 32 + y * 32, 'box_title',
                                        self.map_data.tiledgidmap[self.map_data.get_tile_gid(x, y, 1)])
                        self.all_object.append(t)
                    elif self.map_data.tiledgidmap[self.map_data.get_tile_gid(x, y, 1)] in titles[4]:
                        t = House(self.map_data.get_tile_image(x, y, 1), 550 + x * 56 - y * 56, 120 + x * 32 + y * 32,
                                  self.map_data.tiledgidmap[self.map_data.get_tile_gid(x, y, 1)], level)
                        self.all_object.append(t)
                        house_count += 1
                    elif self.map_data.tiledgidmap[self.map_data.get_tile_gid(x, y, 1)] == 51:
                        Board(self.map_data.get_tile_image(x, y, 1))

        diaminds = random.randint(6, 50)
        for i in range(diaminds):
            x, y = random.randint(0, self.width), random.randint(0, self.height)
            while (x, y) in self.obstacles and (x, y) not in self.tiles:
                x, y = random.randint(0, self.width), random.randint(0, self.height)
            d = Diamond(550 + x * 56 - y * 56, 120 + x * 32 + y * 32)
            if not pygame.sprite.spritecollideany(d, tiles_group):
                d.kill()
                diaminds += 1
            elif pygame.sprite.spritecollideany(d, tiles_group):
                self.obstacles.append((x, y))
                self.all_object.append(d)
        ore = random.randint(6, 20)
        for i in range(ore):
            x, y = random.randint(0, self.width), random.randint(0, self.height // 2)
            while (x, y) in self.obstacles:
                x, y = random.randint(0, self.width), random.randint(0, self.height // 2)
            if level == 1:
                i = 'ore_deposits2'
            elif level == 2:
                i = 'ore_deposits3'
            elif level == 3:
                i = 'ore_deposits4'
            p = PolylineObj(550 + x * 56 - y * 56, 120 + x * 32 + y * 32, i)
            if not pygame.sprite.spritecollideany(p, tiles_group):
                p.kill()
            elif pygame.sprite.spritecollideany(p, tiles_group):
                ore_group.add(p)
                self.all_object.append(p)
        screen.blit(pygame.transform.scale(display, screen.get_size()), (0, 0))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

    def more_ore(self):
        self.ore = random.randint(6, 20)
        for i in range(self.ore):
            x, y = random.randint(0 - self.width // 2, self.width // 2), random.randint(0 - self.height // 2,
                                                                                        self.height // 2)
            x += camera.dx
            y += camera.dy
            if level == 1:
                i = 'ore_deposits2'
            elif level == 2:
                i = 'ore_deposits3'
            elif level == 3:
                i = 'ore_deposits4'
            p = PolylineObj(550 + x * 56 - y * 56, 120 + x * 32 + y * 32, i)
            if not pygame.sprite.spritecollideany(p, tiles_group):
                p.kill()
            elif pygame.sprite.spritecollideany(p, tiles_group):
                self.all_object.append(p)

    def more_dimond(self):
        global camera
        self.diaminds = random.randint(6, 50)
        for i in range(self.diaminds):
            x, y = random.randint(0 - self.width // 2, self.width // 2), random.randint(0 - self.height // 2,
                                                                                        self.height // 2)
            x += camera.dx
            y += camera.dy
            d = Diamond(550 + x * 56 - y * 56, 120 + x * 32 + y * 32)
            if not pygame.sprite.spritecollideany(d, tiles_group) or (
                    (x, y) in self.obstacles and (x, y) not in self.tiles):
                d.kill()
            elif pygame.sprite.spritecollideany(d, tiles_group):
                self.obstacles.append((x, y))
                self.all_object.append(d)


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
        self.image_strel2 = pygame.transform.rotate(self.image_strel, 180)
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
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if self.count == 1:
                        if 900 < x < 970 and 550 < y < 620:
                            self.click_sound.play()
                            self.instruction2()
                            running = False
                    elif self.count == 2:
                        if 900 < x < 970 and 550 < y < 620:
                            self.click_sound.play()
                            self.instruction3()
                            running = False
                        if 20 < x < 90 and 550 < y < 620:
                            self.click_sound.play()
                            self.instruction1()
                            running = False
                    elif self.count == 3:
                        if 900 < x < 970 and 550 < y < 620:
                            self.click_sound.play()
                            running = False
                        if 20 < x < 90 and 550 < y < 620:
                            self.click_sound.play()
                            self.instruction2()
                            running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        if self.count == 1:
                            self.click_sound.play()
                            self.instruction2()
                            running = False
                        elif self.count == 2:
                            self.click_sound.play()
                            self.instruction3()
                            running = False
                        elif self.count == 3:
                            self.click_sound.play()
                            running = False
                    elif event.key == pygame.K_LEFT:
                        if self.count == 2:
                            self.click_sound.play()
                            self.instruction1()
                            running = False
                        elif self.count == 3:
                            self.click_sound.play()
                            self.instruction2()
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
        self.text_coord = 50
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
        image_depos = pygame.transform.scale(load_image("dop_deposits2.png", (255, 255, 255), f='images'), (90, 110))
        image_box = pygame.transform.scale(load_image("dop_box.png", (255, 255, 255), f='images'), (90, 100))
        self.count = 2
        display.fill((255, 248, 231))
        screen.blit(pygame.transform.scale(display, screen.get_size()), (0, 0))
        screen.blit(self.text, (320, 4))
        screen.blit(self.image_strel, (900, 550))
        screen.blit(self.image_strel2, (20, 550))
        screen.blit(image_diam, (15, 190))
        screen.blit(image_depos, (15, 310))
        screen.blit(image_box, (15, 450))
        pygame.display.update()
        opis_text = ["Цель этой игры - заработать как можно больше монеток, чтобы развиваться дальше",
                     "Сейчас вы спросите как же это сделать :з",
                     "Давайте посмотрим"]
        diamon_text = ["Это алмазик, собирая его вы будете получать 10 монеток за каждый",
                       "Чтобы взять алмазик, просто подойдите к нему"]
        depos_text = ["А это один из видов руды. Но ее не так просто собрать",
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
        self.count = 3
        display.fill((255, 248, 231))
        screen.blit(pygame.transform.scale(display, screen.get_size()), (0, 0))
        screen.blit(self.text, (320, 4))
        screen.blit(self.image_strel, (900, 550))
        screen.blit(self.image_strel2, (20, 550))
        pygame.display.update()
        opis_text = ["Так же на карте вы встретите дома, которые можно купить и получать одну монетку в секунду",
                     "Купленные дома можно улучшать и тогда они будут приносить на одну монетку больше"]
        upr_text = ["Как же происходит управление?",
                    "Управление происходит с помощьюю клавиш WASD",
                    "W - вверх",
                    "S - вниз",
                    "A - влево",
                    "D - вправо"]
        author_text = ["Над игрой работали Дувакин Андрей и Толменева Дарья",
                       "Удачной игры :з"]
        texts = [opis_text, upr_text, author_text]
        self.text_coord = 50
        for i in texts:
            for line in i:
                string_rendered = self.font2.render(line, True, pygame.Color('black'))
                intro_rect = string_rendered.get_rect()
                intro_rect.x = 10
                self.text_coord += 10
                intro_rect.top = self.text_coord
                self.text_coord += intro_rect.height
                screen.blit(string_rendered, intro_rect)
                pygame.display.update()
            self.text_coord += 30
        self.running()


class Final():
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
        self.fon = pygame.image.load("data/images/fon_or.png")
        self.font = pygame.font.Font('data/fonts/font.otf', 90)
        self.normal_font = pygame.font.Font('data/fonts/Impact.ttf', 18)
        self.text = self.font.render("Dinosaur Settlement", True, (171, 195, 87))
        self.text2 = self.normal_font.render('Спасибо, что играли в нашу игру!', True, (171, 195, 87))
        self.count = 0
        self.time = 0
        self.h = 0
        self.go_final()

    def go_final(self):
        running = True
        while running:
            screen.fill((255, 255, 255))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            if self.time < 20:
                self.draw_name()
            if 8 < self.time < 20:
                self.draw_res()
            self.timer.tick(120)
            self.time += 1 / 6

    def draw_res(self):
        global display
        if self.time < 20:
            self.h2 = 5
        elif self.time >= 20:
            self.h2 = 0
        screen.blit(self.text2, (10, 250))
        pygame.display.update()

    def draw_name(self):
        global display
        if self.time > 4:
            self.h += 5
        display.fill((255, 255, 255))
        if self.count == 0:
            display.blit(self.im1, (220, 100))
        elif self.count == 1:
            display.blit(self.im2, (220, 100))
        elif self.count == 2:
            display.blit(self.im3, (220, 100))
        elif self.count == 3:
            display.blit(self.im4, (220, 100))
        screen.blit(pygame.transform.scale(display, screen.get_size()), (0, 0 - self.h))
        screen.blit(self.text, (40, 250 - self.h))
        pygame.display.update()
        self.timer.tick(7)
        self.count = (self.count + 1) % 4


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


def insert_base(level, money, time):
    con = sqlite3.connect("data/base/data.sqlite")
    cur = con.cursor()
    cur.execute("""INSERT INTO main(level, money, sessiontime) VALUES(?, ?, ?)""",
                (item_id := int(level), int(money), abs(int(time))))
    con.commit()
    con.close()


def tertius_level():
    global level
    global play_sound
    global money
    global camera
    global stat_time
    if play_sound:
        play_sound = True
    else:
        play_sound = False
    ostrov = Ostrov()
    ostrov.draw()
    player = Player(-450, 2000)
    money_img = load_image("money_img.jpg", (255, 255, 255), f='images')
    money_img = pygame.transform.scale(money_img, (30, 30))
    money_fon = pygame.transform.scale(load_image("new_money_fon.png", (0, 0, 0), f='images'), (350, 50))
    running = True
    clock = pygame.time.Clock()
    board = pygame.transform.scale(load_image('fon_board_house.png', (0, 0, 0), f='images'), (205, 145))
    fon = pygame.image.load("data/images/fon_or.png")
    stop_but = pygame.transform.scale(load_image("no_sound.png", convert=False, f='images'), (40, 40))
    font = pygame.font.Font('data/fonts/font.otf', 50)
    font_medium = pygame.font.Font('data/fonts/Impact.ttf', 15)
    text1 = font_medium.render('Ты можешь перейти ', True, (255, 255, 255))
    text2 = font_medium.render('на следующий уровень!', True, (255, 255, 255))
    level_but = pygame.transform.scale(load_image('level_button.png', (0, 0, 0), f='images'), (185, 75))
    play_but = pygame.transform.scale(load_image("sound.png", convert=False, f='images'), (40, 40))
    new_level = False
    all = [board, fon, stop_but, font, font_medium, text1, text2, level_but, play_but]
    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                insert_base(level, money, stat_time - time.time())
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if (pos[0] > 880 and pos[0] < 980) and (pos[1] > 20 and pos[1] < 80) and play_sound:
                    play_sound = False
                    sound.stop()
                elif (pos[0] > 880 and pos[0] < 980) and (pos[1] > 20 and pos[1] < 80) and not play_sound:
                    play_sound = True
                    sound.play()
                if money >= 120000:
                    x, y = pos
                    if cat.active_task:
                        if 10 < x < 195 and 250 < y < 325:
                            new_level = True
                    else:
                        if 10 < x < 195 and 110 < y < 185:
                            new_level = True
        camera.update(player)
        for sprite in all_sprites:
            camera.apply(sprite)
        if len(diamond_group) <= ostrov.diaminds or len(diamond_group) <= 9:
            ostrov.more_dimond()
        if len(ore_group) <= ostrov.ore or len(ore_group) <= 9:
            ostrov.more_ore()
        screen.blit(fon, (0, 0))
        all_sprites.draw(screen)
        all_sprites.update()
        big_obstacles_group.draw(screen)
        cat_group.draw(screen)
        cat_group.update()
        player_group.update()
        house_group.update()
        screen.blit(money_fon, (0, 0))
        if money >= 750000:
            if cat.active_task:
                screen.blit(board, (0, 200))
                screen.blit(text1, (10, 210))
                screen.blit(text2, (10, 225))
                screen.blit(level_but, (10, 250))
            else:
                screen.blit(board, (0, 50))
                screen.blit(text1, (20, 65))
                screen.blit(text2, (20, 80))
                screen.blit(level_but, (10, 110))
        if new_level:
            insert_base(level, money, stat_time - time.time())
            level = 4
            money = 100
            for i in all_sprites:
                i.kill()
            for i in all:
                i = 0
            break
        text = font.render(f"{str(int(money))}", True, (255, 255, 255))
        screen.blit(text, (66, 4))
        screen.blit(money_img, (30, 10))
        if play_sound:
            screen.blit(play_but, (900, 20))
        else:
            screen.blit(stop_but, (900, 20))
        pygame.display.flip()
        clock.tick(FPS)


def second_level():
    global level
    global play_sound
    global money
    global camera
    global stat_time
    if play_sound:
        play_sound = True
    else:
        play_sound = False
    ostrov = Ostrov()
    ostrov.draw()
    player = Player(350, 1600)
    money_img = load_image("money_img.jpg", (255, 255, 255), f='images')
    money_img = pygame.transform.scale(money_img, (30, 30))
    money_fon = pygame.transform.scale(load_image("new_money_fon.png", (0, 0, 0), f='images'), (350, 50))
    running = True
    clock = pygame.time.Clock()
    board = pygame.transform.scale(load_image('fon_board_house.png', (0, 0, 0), f='images'), (205, 145))
    fon = pygame.image.load("data/images/fon_or.png")
    stop_but = pygame.transform.scale(load_image("no_sound.png", convert=False, f='images'), (40, 40))
    font = pygame.font.Font('data/fonts/font.otf', 50)
    font_medium = pygame.font.Font('data/fonts/Impact.ttf', 15)
    text1 = font_medium.render('Ты можешь перейти ', True, (255, 255, 255))
    text2 = font_medium.render('на следующий уровень!', True, (255, 255, 255))
    level_but = pygame.transform.scale(load_image('level_button.png', (0, 0, 0), f='images'), (185, 75))
    play_but = pygame.transform.scale(load_image("sound.png", convert=False, f='images'), (40, 40))
    new_level = False
    all = [board, fon, stop_but, font, font_medium, text1, text2, level_but, play_but]
    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                insert_base(level, money, stat_time - time.time())
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if (pos[0] > 880 and pos[0] < 980) and (pos[1] > 20 and pos[1] < 80) and play_sound:
                    play_sound = False
                    sound.stop()
                elif (pos[0] > 880 and pos[0] < 980) and (pos[1] > 20 and pos[1] < 80) and not play_sound:
                    play_sound = True
                    sound.play()
                if money >= 120000:
                    x, y = pos
                    if cat.active_task:
                        if 10 < x < 195 and 250 < y < 325:
                            new_level = True
                    else:
                        if 10 < x < 195 and 110 < y < 185:
                            new_level = True
        camera.update(player)
        for sprite in all_sprites:
            camera.apply(sprite)
        if len(diamond_group) <= ostrov.diaminds or len(diamond_group) <= 9:
            ostrov.more_dimond()
        if len(ore_group) <= ostrov.ore or len(ore_group) <= 9:
            ostrov.more_ore()
        screen.blit(fon, (0, 0))
        all_sprites.draw(screen)
        all_sprites.update()
        big_obstacles_group.draw(screen)
        cat_group.draw(screen)
        cat_group.update()
        player_group.update()
        house_group.update()
        screen.blit(money_fon, (0, 0))
        if money >= 370000:
            if cat.active_task:
                screen.blit(board, (0, 200))
                screen.blit(text1, (10, 210))
                screen.blit(text2, (10, 225))
                screen.blit(level_but, (10, 250))
            else:
                screen.blit(board, (0, 50))
                screen.blit(text1, (20, 65))
                screen.blit(text2, (20, 80))
                screen.blit(level_but, (10, 110))
        if new_level:
            insert_base(level, money, stat_time - time.time())
            level = 3
            money = 100
            for i in all_sprites:
                i.kill()
            for i in all:
                i = 0
            break
        text = font.render(f"{str(int(money))}", True, (255, 255, 255))
        screen.blit(text, (66, 4))
        screen.blit(money_img, (30, 10))
        if play_sound:
            screen.blit(play_but, (900, 20))
        else:
            screen.blit(stop_but, (900, 20))
        pygame.display.flip()
        clock.tick(FPS)


def start_game():
    global level
    global play_sound
    global money
    global camera
    global stat_time
    ostrov = Ostrov()
    ostrov.draw()
    if play_sound:
        play_sound = True
    else:
        play_sound = False
    player = Player(350, 1600)
    money_img = load_image("money_img.jpg", (255, 255, 255), f='images')
    money_img = pygame.transform.scale(money_img, (30, 30))
    money_fon = pygame.transform.scale(load_image("new_money_fon.png", (0, 0, 0), f='images'), (350, 50))
    running = True
    clock = pygame.time.Clock()
    board = pygame.transform.scale(load_image('fon_board_house.png', (0, 0, 0), f='images'), (205, 145))
    fon = pygame.image.load("data/images/fon_or.png")
    stop_but = pygame.transform.scale(load_image("no_sound.png", convert=False, f='images'), (40, 40))
    font = pygame.font.Font('data/fonts/font.otf', 50)
    font_medium = pygame.font.Font('data/fonts/Impact.ttf', 15)
    text1 = font_medium.render('Ты можешь перейти ', True, (255, 255, 255))
    text2 = font_medium.render('на следующий уровень!', True, (255, 255, 255))
    level_but = pygame.transform.scale(load_image('level_button.png', (0, 0, 0), f='images'), (185, 75))
    play_but = pygame.transform.scale(load_image("sound.png", convert=False, f='images'), (40, 40))
    new_level = False
    all = [board, fon, stop_but, font, font_medium, text1, text2, level_but, play_but]
    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                insert_base(level, money, stat_time - time.time())
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if (pos[0] > 880 and pos[0] < 980) and (pos[1] > 20 and pos[1] < 80) and play_sound:
                    play_sound = False
                    sound.stop()
                elif (pos[0] > 880 and pos[0] < 980) and (pos[1] > 20 and pos[1] < 80) and not play_sound:
                    play_sound = True
                    sound.play()
                if money >= 200000:
                    x, y = pos
                    if cat.active_task:
                        if 10 < x < 195 and 250 < y < 325:
                            new_level = True
                    else:
                        if 10 < x < 195 and 110 < y < 185:
                            new_level = True
        camera.update(player)
        for sprite in all_sprites:
            camera.apply(sprite)
        if len(diamond_group) <= ostrov.diaminds or len(diamond_group) <= 9:
            ostrov.more_dimond()
        if len(ore_group) <= ostrov.ore or len(ore_group) <= 9:
            ostrov.more_ore()
        screen.blit(fon, (0, 0))
        all_sprites.draw(screen)
        all_sprites.update()
        big_obstacles_group.draw(screen)
        cat_group.draw(screen)
        cat_group.update()
        player_group.update()
        screen.blit(money_fon, (0, 0))
        if money >= 200000:
            if cat.active_task:
                screen.blit(board, (0, 200))
                screen.blit(text1, (10, 210))
                screen.blit(text2, (10, 225))
                screen.blit(level_but, (10, 250))
            else:
                screen.blit(board, (0, 50))
                screen.blit(text1, (20, 65))
                screen.blit(text2, (20, 80))
                screen.blit(level_but, (10, 110))
        if new_level:
            insert_base(level, money, stat_time - time.time())
            level = 2
            money = 100
            for i in all_sprites:
                i.kill()
            for i in all:
                i = 0
            break
        text = font.render(f"{str(int(money))}", True, (255, 255, 255))
        cat_group.update()
        screen.blit(text, (66, 4))
        screen.blit(money_img, (30, 10))
        if play_sound:
            screen.blit(play_but, (900, 20))
        else:
            screen.blit(stop_but, (900, 20))
        pygame.display.flip()
        clock.tick(FPS)


def play():
    global cat
    if level == 1:
        cat = Cat(2530, 1380)
        dow.draw()
        start_game()
    if level == 2:
        cat = Cat(440, 2400)
        dow.draw()
        second_level()
    if level == 3:
        cat = Cat(1449, 860)
        dow.draw()
        tertius_level()
    if level == 4:
        Final()


pygame.display.set_caption('DinosaurSettlement')
sound = pygame.mixer.Sound('data/musics/Music.mp3')
sound.play()
stat_time = time.time()
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
camera = Camera()
instruction = Instruction()
instruction.instruction1()
dow = Dowload()
play()