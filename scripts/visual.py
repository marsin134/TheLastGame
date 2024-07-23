import pygame
import os
import sys
from random import choice
from scripts import constants as CONST

pygame.init()

# required constants
SCREEN_WIDTH, SCREEN_HEIGHT = CONST.SCREEN_WIDTH, CONST.SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
TILE_SIZE = TILE_WIDTH, TILE_HEIGHT = CONST.TILE_WIDTH, CONST.TILE_HEIGHT

# short block designations
dict_tile = {'#': 'mud_block2.png',
             ',': 'mud_block4.png',
             '.': 'mud_block3.png',
             '-': 'mud_platform.png',
             '/': 'mud_platform_left.png',
             '//': 'mud_platform_right.png',
             '|': 'ladder.png',
             'b': 'bush.png',
             'w': 'wood.png',
             '!': 'statue.png',
             's': 'stone.png'}


# class blocks
class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, *groups, size=TILE_SIZE):
        super().__init__(*groups)
        self.image = load_image(f'facilities/{dict_tile[tile_type]}', transforms=size)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(
            TILE_WIDTH * pos_x, TILE_HEIGHT * pos_y)


# class clouds
class Clouds(pygame.sprite.Sprite):
    def __init__(self, *groups, pos_x=-TILE_WIDTH * 4.5):
        super().__init__(*groups)

        self.image = load_image(f'facilities/{choice(clouds_list_name)}', colorkey=-1,
                                transforms=(TILE_WIDTH * 4.5, TILE_HEIGHT * 1.8))
        self.rect = self.image.get_rect().move(pos_x, choice(range(0, 76, 25)))

        self.shaking = 3

    def update(self):
        # If you went outside the world
        if self.rect.x > SCREEN_WIDTH + TILE_WIDTH * 4.5:
            self.kill()

        self.rect.x += 2

        #  Shaking the clouds
        if self.rect.x % 20 == 0:
            self.rect.y += self.shaking
            self.shaking *= -1


def load_image(name, colorkey=None, transforms=None):
    # download image

    fullname = os.path.join('data/image', name)
    # if the file does not exist, then exit
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)

    # removing the background
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()

    # changing the size
    if transforms:
        image = pygame.transform.scale(image, transforms)
    return image


def create_platform(pos_x, pos_y, length_platform=2):
    # creating a left border
    Tile('/', pos_x, pos_y, tiles_group, all_sprites, size=(TILE_WIDTH * 2, TILE_HEIGHT * 2))

    # creating a platform
    for platform in range(0, length_platform * 2 - 2, + 2):
        Tile('-', pos_x + 1 + platform, pos_y, tiles_group, all_sprites, size=(TILE_WIDTH * 2, TILE_HEIGHT * 2))

    # creating the right border
    Tile('//', pos_x + length_platform * 2 - 1, pos_y, tiles_group, all_sprites, size=(TILE_WIDTH * 2, TILE_HEIGHT * 2))

    # creating ladders on platforms
    for platform in range(0, length_platform * 2, + 2):
        Tile('|', pos_x + platform, pos_y, all_sprites, size=(TILE_WIDTH * 2, TILE_HEIGHT * 2))

    # creating the last ladder on the platform
    Tile('|', pos_x + length_platform * 2, pos_y, all_sprites, size=(TILE_WIDTH, TILE_HEIGHT * 2))


def create_map():
    # Creation of the earth
    for i in range(SCREEN_WIDTH // TILE_WIDTH + 2):
        Tile('#', i, SCREEN_HEIGHT // TILE_HEIGHT - 2, tiles_group, all_sprites)
        Tile(',', i, SCREEN_HEIGHT // TILE_HEIGHT - 1, all_sprites)
        Tile('.', i, SCREEN_HEIGHT // TILE_HEIGHT, all_sprites)

    create_platform(4, 12, 5)
    create_platform(26, 12, 5)

    # creating a decor
    Tile('b', 11, 11, all_sprites, size=(TILE_WIDTH * 3, TILE_HEIGHT))
    Tile('b', 5, 11, all_sprites, size=(TILE_WIDTH * 3, TILE_HEIGHT))
    Tile('w', 6.5, 11 - 4.8, all_sprites, size=(TILE_WIDTH * 6, TILE_HEIGHT * 6))

    Tile('b', 33, 11, all_sprites, size=(TILE_WIDTH * 3, TILE_HEIGHT))
    Tile('b', 27, 11, all_sprites, size=(TILE_WIDTH * 3, TILE_HEIGHT))
    Tile('w', 28.5, 11 - 4.8, all_sprites, size=(TILE_WIDTH * 6, TILE_HEIGHT * 6))

    Tile('w', 25, SCREEN_HEIGHT // TILE_HEIGHT - 7.8, all_sprites, size=(TILE_WIDTH * 6, TILE_HEIGHT * 6))
    Tile('w', 11, SCREEN_HEIGHT // TILE_HEIGHT - 7.8, all_sprites, size=(TILE_WIDTH * 6, TILE_HEIGHT * 6))

    Tile('s', 16, SCREEN_HEIGHT // TILE_HEIGHT - 3, all_sprites, size=(TILE_WIDTH * 2, TILE_HEIGHT))
    Tile('s', 23, SCREEN_HEIGHT // TILE_HEIGHT - 3, all_sprites, size=(TILE_WIDTH * 2, TILE_HEIGHT))

    Tile('b', 9, SCREEN_HEIGHT // TILE_HEIGHT - 3, all_sprites, size=(TILE_WIDTH * 3, TILE_HEIGHT))
    Tile('b', 30, SCREEN_HEIGHT // TILE_HEIGHT - 3, all_sprites, size=(TILE_WIDTH * 3, TILE_HEIGHT))

    # creating a clouds
    for i in range(0, SCREEN_WIDTH, +TILE_WIDTH * 4):
        Clouds(clouds_group, all_sprites, pos_x=i)


def display_text(surface, user_text, scale, transparency):
    font = pygame.font.Font('data/fonts/Stefan Stoychev - Block Light.ttf', scale)
    text = font.render(user_text, False, (0, 0, 0))

    text.convert_alpha()
    text.set_alpha(transparency)

    pos_x = SCREEN_WIDTH // 2 - len(user_text) * scale // 5.5
    pos_y = SCREEN_HEIGHT // 2 - scale * 3 // 2

    surface.blit(text, (pos_x, pos_y))


# different variations of clouds
clouds_list_name = ['clouds1.png', 'clouds2.png', 'clouds3.png']

# creating sprites, maps and backgrounds
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
clouds_group = pygame.sprite.Group()

create_map()

fon_game = load_image('fons/fon_game.png', transforms=(SCREEN_WIDTH, SCREEN_HEIGHT))
fon_lose = load_image('fons/lose_fon.png', transforms=(SCREEN_WIDTH, SCREEN_HEIGHT))
fon_win = load_image('fons/win_fon.png', transforms=(SCREEN_WIDTH, SCREEN_HEIGHT))

image_grey = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
image_grey.fill((128, 128, 128))
image_grey.set_colorkey((0, 0, 0))
image_grey.set_alpha(30)
