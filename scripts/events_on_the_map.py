import pygame
from scripts.visual import load_image
from scripts.constants import TILE_WIDTH, TILE_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT, fire_anim, quantity_fire
from random import choice
from scripts.enemy import Goblin, FlyingEye, Skeleton, Mushroom


class Statue(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)

        pos_x, pos_y = (SCREEN_WIDTH // TILE_WIDTH) // 2 - 1.2, SCREEN_HEIGHT // TILE_HEIGHT - 8

        self.image = load_image('facilities/statue.png', transforms=(TILE_WIDTH * 4, TILE_HEIGHT * 6))
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect().move(
            TILE_WIDTH * pos_x, TILE_HEIGHT * pos_y)

        self.heath_start = self.hp = 25

        self.hit = False

    def update(self, surface):
        if self.hp <= 0:
            self.kill()

        else:
            # coordinates_list = [start_x, start_y, duration_x, duration_y, end_x]
            coordinates_list = [self.rect.x + 20, self.rect.y - 12 + self.rect[3], self.rect[2] - 40, 10,
                                self.rect.x - 20 + self.rect[2]]

            pygame.draw.rect(surface, (64, 0, 0),
                             (coordinates_list[0], coordinates_list[1], coordinates_list[2], coordinates_list[3]))

            pygame.draw.rect(surface, (0, 64, 0),
                             (coordinates_list[0], coordinates_list[1],
                              coordinates_list[2] * (self.hp / self.heath_start),
                              coordinates_list[3]))

        self.hit = False


class Fire(pygame.sprite.Sprite):
    def __init__(self, person, tiles, *group):
        super().__init__(*group)
        self.frames = []
        self.cur_frame = 0
        self.index = 0

        self.person = person

        self.update_time_anim = pygame.time.get_ticks()

        self.update_time_fire = pygame.time.get_ticks()
        self.cooldown_fire = 10000

        self.variations = choice(['green', 'purple', 'white'])
        # self.variations = 'white'

        self.cut_sheet([(f'{self.variations}/start/burning_start_1.png', 4),
                        (f'{self.variations}/loops/burning_loop_1.png', 8),
                        (f'{self.variations}/end/burning_end_1.png', 5)])

        self.image = self.frames[0][self.cur_frame]

        tile = random_tile(tiles)
        self.rect = self.image.get_rect().move(tile.rect.x, tile.rect.y - TILE_HEIGHT)

        self.mask = pygame.mask.from_surface(self.image)

        self.cooldown_anim = fire_anim

    def cut_sheet(self, list_sheet):
        sheet = load_image(f'fire/{list_sheet[0][0]}')
        self.rect = pygame.Rect(0, 0, sheet.get_width() // list_sheet[0][1], sheet.get_height())

        for i in range(len(list_sheet)):
            sheet = load_image(f'fire/{list_sheet[i][0]}')
            frame_list = []
            for j in range(list_sheet[i][1]):
                self.rect = pygame.Rect(0, 0, sheet.get_width() // list_sheet[i][1], sheet.get_height())

                frame_location = (self.rect.w * j, 0)
                frame_list.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))
            self.frames.append(frame_list)

    def update_sheet(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames[self.index])
        self.image = self.frames[self.index][self.cur_frame]
        self.mask = pygame.mask.from_surface(self.image)

        if self.index == 0 and (self.cur_frame + 1) % len(self.frames[self.index]) == 0:
            self.index = 1

        elif self.index == 2 and (self.cur_frame + 1) % len(self.frames[self.index]) == 0:
            self.kill()

    def update(self, surface):
        if pygame.sprite.collide_mask(self, self.person) and self.index == 1:
            self.index = 2
            self.cur_frame = 0
            if self.variations == 'green':
                self.person.hp = self.person.heath_start // 2 + self.person.hp if (
                                                                                          self.person.hp + self.person.heath_start // 2) // self.person.heath_start == 0 \
                    else self.person.heath_start
            elif self.variations == 'purple':
                self.person.attack_power = round(self.person.attack_power * 1.2, 4)
            elif self.variations == 'white':
                self.person.heath_start = round(self.person.heath_start * 1.1, 4)

        if pygame.time.get_ticks() - self.update_time_anim > self.cooldown_anim:
            self.update_time_anim = pygame.time.get_ticks()
            self.update_sheet()

        if pygame.time.get_ticks() - self.update_time_fire > self.cooldown_fire and self.index == 1:
            self.index = 2
            self.cur_frame = 0

        surface.blit(self.image, self.rect)


class Wave:
    def __init__(self, statue, player, tiles_group, enemy_group):
        self.number_waves = 0

        self.statue = statue
        self.tiles_group = tiles_group
        self.enemy_group = enemy_group
        self.player = player
        self.fire_group = pygame.sprite.Group()

        self.number_enemyies_in_waves = open('data/txt_files/TheDistributionOfEnemiesOnTheWaves').readlines()[1:]
        self.number_enemyies_in_waves = [[int(number) for number in elem.split()] for elem in
                                         self.number_enemyies_in_waves]

        self.update_time = pygame.time.get_ticks()
        self.cooldown_enemy = 3000
        self.cooldown_wave = 10000

        self.quantity_firs = quantity_fire

        self.dict_enemy = {0: Goblin,
                           1: Skeleton,
                           2: FlyingEye,
                           3: Mushroom}

        # fire creation time
        self.cooldown_fire = 10000
        self.update_time_fire = 0

        self.completed_wave = False

    def update(self, surface):
        if sum(self.number_enemyies_in_waves[self.number_waves]) != 0:
            if pygame.time.get_ticks() - self.update_time > self.cooldown_enemy:
                self.update_time = pygame.time.get_ticks()

                self.random_choose_enemy()

        elif not self.enemy_group:
            if self.completed_wave:
                if pygame.time.get_ticks() - self.update_time > self.cooldown_wave:
                    self.update_time = pygame.time.get_ticks()

                    self.completed_wave = False
            else:
                self.number_waves += 1

                self.statue.hp = self.statue.heath_start
                self.player.hp = self.player.heath_start

                self.update_time = pygame.time.get_ticks()

                self.completed_wave = True

                self.quantity_firs = quantity_fire

        # creating a fire
        if pygame.time.get_ticks() - self.update_time_fire > self.cooldown_fire and self.quantity_firs > 0:
            Fire(self.player, self.tiles_group, self.fire_group)
            self.update_time_fire = pygame.time.get_ticks()
            self.quantity_firs -= 1

        self.fire_group.update(surface)

    def random_choose_enemy(self):
        enemy_index = choice(range(len(self.number_enemyies_in_waves[self.number_waves])))
        while self.number_enemyies_in_waves[self.number_waves][enemy_index] == 0:
            enemy_index = choice(range(len(self.number_enemyies_in_waves[self.number_waves])))
        self.number_enemyies_in_waves[self.number_waves][enemy_index] -= 1
        enemy = self.dict_enemy[enemy_index](
            (choice([-50, SCREEN_WIDTH - 70]), choice([SCREEN_HEIGHT - 250, SCREEN_HEIGHT - 700])),
            self.tiles_group, self.player, self.statue, self.enemy_group)
        self.improvement_enemy(enemy)

    def improvement_enemy(self, enemy):
        enemy.heath_start = enemy.hp = enemy.heath_start * (1 + 0.2 * self.number_waves)
        enemy.attack_power = enemy.attack_power * (1 + 0.2 * self.number_waves)


def random_tile(tiles_group):
    # retrieves a random object from a group
    iteration = 2
    index = choice(range(iteration, len(tiles_group) - iteration))
    for tile in tiles_group:
        if iteration == index:
            return tile
        iteration += 1
