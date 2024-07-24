import pygame
from scripts import visual, menu
from scripts import constants as CONST
from random import choice
from scripts.enemy import Goblin, FlyingEye, Skeleton, Mushroom, DeathEnemy
from scripts.players import is_collided_with
from scripts.boss import BossSoul


class Statue(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)

        pos_x, pos_y = (CONST.SCREEN_WIDTH // CONST.TILE_WIDTH) // 2 - 1.2, CONST.SCREEN_HEIGHT // CONST.TILE_HEIGHT - 8

        self.image = visual.load_image('facilities/statue.png',
                                       transforms=(CONST.TILE_WIDTH * 4, CONST.TILE_HEIGHT * 6))
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect().move(
            CONST.TILE_WIDTH * pos_x, CONST.TILE_HEIGHT * pos_y)

        self.heath_start = self.hp = CONST.statue_hp
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
    def __init__(self, person, tiles, *group, pos=-1):
        super().__init__(*group)
        self.frames = []
        self.cur_frame = 0
        self.index = 0

        self.person = person

        self.update_time_anim = pygame.time.get_ticks()

        self.update_time_fire = pygame.time.get_ticks()
        self.cooldown_fire = CONST.fire_cooldown

        self.variations = choice(['green', 'purple', 'white'])
        # self.variations = 'white'

        self.cut_sheet([(f'{self.variations}/start/burning_start_1.png', 4),
                        (f'{self.variations}/loops/burning_loop_1.png', 8),
                        (f'{self.variations}/end/burning_end_1.png', 5)])

        self.image = self.frames[0][self.cur_frame]

        self.tiles = tiles

        tile = random_tile(tiles)

        if pos == -1:
            self.rect = self.image.get_rect().move(tile.rect.x, tile.rect.y - CONST.TILE_HEIGHT)

        else:
            self.rect = self.image.get_rect().move(pos)

        self.mask = pygame.mask.from_surface(self.image)

        self.cooldown_anim = CONST.fire_anim

    def cut_sheet(self, list_sheet):
        sheet = visual.load_image(f'fire/{list_sheet[0][0]}')
        self.rect = pygame.Rect(0, 0, sheet.get_width() // list_sheet[0][1], sheet.get_height())

        for i in range(len(list_sheet)):
            sheet = visual.load_image(f'fire/{list_sheet[i][0]}')
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
        # if he encounters a player, we improve the player's characteristics
        if pygame.sprite.collide_mask(self, self.person) and self.index == 1:
            fire_sound_collide.play()

            self.index = 2
            self.cur_frame = 0

            if self.variations == 'green':
                self.person.hp = self.person.heath_start // 2 + self.person.hp if (
                                                                                          self.person.hp + self.person.heath_start // 2) // self.person.heath_start == 0 \
                    else self.person.heath_start

            elif self.variations == 'purple':
                difficulty = float(open('data/txt_files/saves.txt', 'r', encoding='utf-8').readlines()[1].split()[-1])
                self.person.attack_power = round(self.person.attack_power * (1 + (0.04 + difficulty / 100)), 4)

            elif self.variations == 'white':
                self.person.heath_start = round(self.person.heath_start * 1.05, 4)

        # updating the animation
        if pygame.time.get_ticks() - self.update_time_anim > self.cooldown_anim:
            self.update_time_anim = pygame.time.get_ticks()
            self.update_sheet()

        # if the fire burns for a long time, we destroy it
        if pygame.time.get_ticks() - self.update_time_fire > self.cooldown_fire and self.index == 1:
            self.index = 2
            self.cur_frame = 0

        # checking to see if there is a fire in the air
        self.rect.y += 3

        if not is_collided_with(self, self.tiles) and self.index == 1:
            # if it is in the air, we destroy the fire
            self.index = 2
            self.cur_frame = 0

        # return the fire to its initial position
        self.rect.y -= 3

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

        self.cooldown_enemy = CONST.cooldown_enemy_spawn
        self.cooldown_wave = CONST.cooldown_wave
        self.update_time = -self.cooldown_enemy // 4

        self.quantity_firs = CONST.quantity_fire

        self.dict_enemy = {0: Goblin,
                           1: Skeleton,
                           2: FlyingEye,
                           3: Mushroom,
                           4: DeathEnemy}

        # fire creation time
        self.cooldown_fire = 10000
        self.update_time_fire = 0

        self.completed_wave = False

        self.scale_frame_text = 0
        self.transparency_text = 1000

        self.death_player = False
        self.win_player = False

        self.boss_fight = False
        self.boss_wave = len(self.number_enemyies_in_waves)

    def update(self, surface):
        # if the user has lost
        if (self.player.hp <= 0 or self.statue.hp <= 0) and not self.death_player:
            self.death_player = True
            self.transparency_text = 0
            pygame.mixer.stop()

        # if the user wins
        if self.win_player and self.scale_frame_text <= 100:
            self.win(surface)
            if self.scale_frame_text < 100:
                self.scale_frame_text += 2
                self.transparency_text += 10
            else:
                menu.exit_in_pause.update(surface)

        # if the user lose
        elif self.death_player and self.scale_frame_text <= 100:
            self.lose(surface)
            if self.scale_frame_text < 100:
                self.scale_frame_text += 2
                self.transparency_text += 10
            else:
                menu.exit_in_pause.update(surface)

        # otherwise, update the wave
        else:
            # if it's not boos fight now and there are still enemies on the wave
            if not self.boss_fight and sum(self.number_enemyies_in_waves[self.number_waves]) != 0:
                if pygame.time.get_ticks() - self.update_time > self.cooldown_enemy:
                    self.update_time = pygame.time.get_ticks()

                    self.random_choose_enemy()

            # If all the enemies died on the wave
            elif not self.enemy_group:

                # if the boss is fighting now, then the user has won
                if self.boss_fight:
                    self.win_player = True
                    self.transparency_text = 0
                    pygame.mixer.stop()

                # Otherwise, create a new wave
                else:
                    if self.completed_wave:
                        self.show_label(surface)

                        if pygame.time.get_ticks() - self.update_time > self.cooldown_wave:
                            self.update_time = -self.cooldown_enemy
                            self.completed_wave = False
                            self.reset_characteristics()
                    else:
                        self.completed_wave = True

                        self.update_time = pygame.time.get_ticks()

                        self.scale_frame_text = 0
                        self.transparency_text = 1000

            self.creating_fire()

            self.fire_group.update(surface)

        if len(str(CONST.money)) > 6:
            CONST.money = 999999

    def random_choose_enemy(self):
        # Chooses a random enemy
        enemy_index = choice(range(len(self.number_enemyies_in_waves[self.number_waves])))

        # If the enemies of this type are dead, select the type that has not died yet
        while self.number_enemyies_in_waves[self.number_waves][enemy_index] == 0:
            enemy_index = choice(range(len(self.number_enemyies_in_waves[self.number_waves])))

        # subtracting a given type of creature from the array
        self.number_enemyies_in_waves[self.number_waves][enemy_index] -= 1

        # Creating an enemy
        enemy = self.dict_enemy[enemy_index](
            (choice(CONST.enemy_spawn_x), choice(CONST.enemy_spawn_y)),
            self.tiles_group, self.player, self.statue, self.enemy_group)

        # We improve the opponent according to the wave
        self.improvement_enemy(enemy)

    def improvement_enemy(self, enemy):
        difficulty = float(open('data/txt_files/saves.txt', 'r', encoding='utf-8').readlines()[1].split()[-1])
        enemy.heath_start = enemy.hp = enemy.heath_start * (1 + (difficulty * 0.1) * self.number_waves)
        enemy.attack_power = enemy.attack_power * (1 + (difficulty * 0.1) * self.number_waves)

    def lose(self, surface):
        visual.fon_lose.set_alpha(self.transparency_text)

        surface.blit(visual.fon_lose, (0, 0))
        visual.display_text(surface, "You death", self.scale_frame_text, self.transparency_text)

    def win(self, surface):
        visual.fon_win.set_alpha(self.transparency_text)

        surface.blit(visual.fon_win, (0, 0))
        visual.display_text(surface, "You win", self.scale_frame_text, self.transparency_text)

    def show_label(self, surface):
        if self.scale_frame_text <= 48:
            visual.display_text(surface, 'wave complete', self.scale_frame_text, self.transparency_text)
            if self.scale_frame_text < 48:
                self.scale_frame_text += 1
            else:
                self.transparency_text -= 50

    def reset_characteristics(self):
        self.number_waves += 1
        self.quantity_firs = CONST.quantity_fire

        # If there is a wave with the boss now
        if self.number_waves == self.boss_wave:
            BossSoul(self.player, self.statue, self.tiles_group, self.enemy_group)

            self.boss_fight = True
            fon_game_music_waterflame.stop()
            self.quantity_firs = CONST.quantity_fire * 2

        self.statue.heath_start = self.statue.hp = CONST.statue_hp * self.number_waves * 0.5
        self.player.hp = self.player.heath_start

    def creating_fire(self):
        # creating a fire
        if pygame.time.get_ticks() - self.update_time_fire > self.cooldown_fire and self.quantity_firs > 0:
            Fire(self.player, self.tiles_group, self.fire_group)
            self.update_time_fire = pygame.time.get_ticks()
            self.quantity_firs -= 1

        if self.player.player_index == 0 and self.player.first_ability_activate:
            if self.quantity_firs > 0:
                Fire(self.player, self.tiles_group, self.fire_group,
                     pos=(self.player.rect.x + CONST.TILE_WIDTH, self.player.rect.y + CONST.TILE_HEIGHT * 3))
                self.quantity_firs -= 1
            self.player.first_ability_activate = False


def random_tile(tiles_group):
    # retrieves a random object from a group
    iteration = 2
    index = choice(range(iteration, len(tiles_group) - iteration))
    for tile in tiles_group:
        if iteration == index:
            return tile
        iteration += 1


fon_game_music_waterflame = pygame.mixer.Sound('data/music/Waterflame fon music.mp3')
fire_sound_collide = pygame.mixer.Sound('data/music/mixkit-light-spell-873.wav')

fon_game_music_waterflame.set_volume(0.85)
fire_sound_collide.set_volume(0.5)
