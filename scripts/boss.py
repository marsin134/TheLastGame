import pygame
from scripts import constants as CONST
from scripts.visual import load_image
from scripts.enemy import Portal
from random import choice


class BossSoul(pygame.sprite.Sprite):
    def __init__(self, person, statue, tiles, *group):
        super().__init__(*group)
        difficulty = float(open('data/txt_files/saves.txt', 'r', encoding='utf-8').readlines()[1].split()[-1])

        self.frames = []

        self.cut_sheet([('Soul_idle.png', 5),
                        ('Soul_attack.png', 10),
                        ('Soul_death.png', 8),
                        ('Soul_move.png', 8)])

        self.cur_frame = 0
        self.index = 0

        self.image = self.frames[0][self.cur_frame]
        self.rect = self.image.get_rect().move(CONST.SCREEN_WIDTH // 2.25, -200)

        self.vx, self.vy = CONST.bossSoul_speeds, CONST.bossSoul_speeds

        self.update_time_anim = pygame.time.get_ticks()
        self.cooldown_anim = 75

        self.cooldown_stop_moving = CONST.bossSoul_cooldown_stop_moving
        self.update_stop_moving = -self.cooldown_stop_moving

        self.tiles_group = tiles

        self.enemy_group = group[0]

        self.person = person
        self.statue = statue

        self.mask = pygame.mask.from_surface(self.image)

        self.attack_flag = False

        self.flip = False

        self.heath_start = self.hp = CONST.bossSoul_heath * difficulty

        self.hit = False
        self.death = False

        self.points = [(CONST.SCREEN_WIDTH // 2.25, 100),
                       (CONST.SCREEN_WIDTH // 2.25, 250),
                       (CONST.SCREEN_WIDTH - 1080, 100),
                       (CONST.SCREEN_WIDTH - 380, 100),
                       (CONST.SCREEN_WIDTH // 4, 225),
                       (CONST.SCREEN_WIDTH // 1.5, 225)]

        self.index_point = 0

        self.index_stage = 0

        self.dict_stage = {0: self.first_stage,
                           1: self.second_stage,
                           2: self.third_stage}

        boss_sound.play(-1)

    def update(self, surface):
        if self.hp <= 0 and self.index != 2:
            self.death = True
            self.index = 2
            self.cur_frame = 0

            self.attack_flag = False

        surface.blit(self.image, self.rect)
        self.draw_heath(surface)

        self.dict_stage[self.index_stage]()

    def first_stage(self):
        if self.heath_start - self.heath_start // 4 > self.hp:
            Crystal((CONST.SCREEN_WIDTH - 200, 300), self, self.enemy_group)
            Crystal((CONST.SCREEN_WIDTH - 1150, 300), self, self.enemy_group)
            Crystal((CONST.SCREEN_WIDTH - 200, 550), self, self.enemy_group)
            Crystal((CONST.SCREEN_WIDTH - 1150, 550), self, self.enemy_group)

            self.index_stage = 1

        self.hit = False

        if pygame.time.get_ticks() - self.update_time_anim > self.cooldown_anim:
            self.update_time_anim = pygame.time.get_ticks()
            self.update_sheet()

            if self.attack_flag and self.cur_frame == 7:
                Ball((self.rect.x, self.rect.y + self.rect.h // 4), (0, 5), self.person,
                     self.statue, self.tiles_group, self.enemy_group)

        self.moving_towards_the_goal()

    def second_stage(self):
        if self.heath_start - self.heath_start // 1.5 > self.hp:
            self.index_stage = 2

        self.hit = True

        self.index_point = 0
        self.cooldown_stop_moving = CONST.bossSoul_cooldown_stop_moving * 4

        if pygame.time.get_ticks() - self.update_time_anim > self.cooldown_anim:
            self.update_time_anim = pygame.time.get_ticks()
            self.update_sheet()

            if self.attack_flag and self.cur_frame == 7:
                Ball((self.rect.x, self.rect.y + self.rect.h // 4), (0, 5), self.person,
                     self.statue, self.tiles_group, self.enemy_group)

        if choice(range(0, 201)) % 200 == 0:
            Portal((self.person.rect.x, self.person.rect.y - 50), self.person, self.enemy_group)

        self.moving_towards_the_goal()

    def third_stage(self):
        if self.hp <= 0 and self.index != 2:
            self.death = True
            self.cur_frame = 0
            self.index = 2

            difficulty = float(open('data/txt_files/saves.txt', 'r', encoding='utf-8').readlines()[1].split()[-1])
            CONST.money += 100 * round(difficulty)

        self.hit = False

        self.cooldown_stop_moving = CONST.bossSoul_cooldown_stop_moving - 200

        if pygame.time.get_ticks() - self.update_time_anim > self.cooldown_anim:
            if choice(range(0, 16)) % 15 != 0:

                Ball((choice([choice(range(0, CONST.SCREEN_WIDTH // 2 - 175)),
                              choice(range(CONST.SCREEN_WIDTH // 2 + 25, CONST.SCREEN_WIDTH))]), -100),
                     (0, 5), self.person, self.statue, self.tiles_group, self.enemy_group)

            else:
                Ball((choice([-100, CONST.SCREEN_WIDTH + 100]), 200), (choice([-5, 5]), 0),
                     self.person, self.statue, self.tiles_group, self.enemy_group)

            self.update_time_anim = pygame.time.get_ticks()
            self.update_sheet()

            if self.attack_flag and self.cur_frame == 7:
                Ball((self.rect.x, self.rect.y + self.rect.h // 4), (0, 5), self.person,
                     self.statue, self.tiles_group, self.enemy_group)

        if choice(range(0, 351)) % 350 == 0:
            Portal((self.person.rect.x, self.person.rect.y - 50), self.person, self.enemy_group)

        self.moving_towards_the_goal()

    def moving_towards_the_goal(self):
        if pygame.time.get_ticks() - self.update_stop_moving > self.cooldown_stop_moving and not self.death:
            self.index = 3

            if not self.rect.x - self.vx <= self.points[self.index_point][0] <= self.rect.x + self.vx:
                if self.rect.x < self.points[self.index_point][0]:
                    self.rect.x += self.vx
                    self.flip = False
                else:
                    self.rect.x -= self.vx
                    self.flip = True

            if not self.rect.y - self.vy <= self.points[self.index_point][1] <= self.rect.y + self.vy:
                if self.rect.y < self.points[self.index_point][1]:
                    self.rect.y += self.vy
                else:
                    self.rect.y -= self.vy

            if (self.rect.x - self.vx <= self.points[self.index_point][0] <= self.rect.x + self.vx
                    and self.rect.y - self.vy <= self.points[self.index_point][1] <= self.rect.y + self.vy):
                self.index_point = choice(range(0, len(self.points)))

                self.update_stop_moving = pygame.time.get_ticks()

                self.attack_flag = True

                self.index = 1
                self.cur_frame = 0

    def cut_sheet(self, list_sheet):
        sheet = load_image(f'enemy/boss/{list_sheet[0][0]}')
        self.rect = pygame.Rect(0, 0, sheet.get_width(), sheet.get_height() // list_sheet[0][1])

        for i in range(len(list_sheet)):
            sheet = load_image(f'enemy/boss/{list_sheet[i][0]}')
            frame_list = []
            for j in range(list_sheet[i][1]):
                self.rect = pygame.Rect(0, 0, sheet.get_width(), sheet.get_height() // list_sheet[i][1])

                frame_location = (0, self.rect.h * j)
                frame_list.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))
            self.frames.append(frame_list)

    def update_sheet(self):
        # if the animation is over
        if (self.cur_frame + 1) % len(self.frames[self.index]) == 0:
            if self.death:
                self.kill()

            elif self.attack_flag:
                self.attack_flag = False

                self.index = 0

        self.cur_frame = (self.cur_frame + 1) % len(self.frames[self.index])
        self.image = self.frames[self.index][self.cur_frame]
        if self.flip:
            self.image = pygame.transform.flip(self.image, True, False)
        self.mask = pygame.mask.from_surface(self.image)

    def draw_heath(self, surface):
        coordinates_list = [self.rect.x + self.rect[2] // 2.75, self.rect.y + self.rect[3] // 5.5, self.rect[2] * 0.25,
                            5,
                            self.rect.x - 20 + self.rect[2]]

        pygame.draw.rect(surface, (64, 0, 0),
                         (coordinates_list[0], coordinates_list[1], coordinates_list[2], coordinates_list[3]))

        pygame.draw.rect(surface, (0, 128, 0),
                         (coordinates_list[0], coordinates_list[1],
                          coordinates_list[2] * (self.hp / self.heath_start),
                          coordinates_list[3]))


class Ball(pygame.sprite.Sprite):
    def __init__(self, pos, array_speed, person, statue, tiles, *group):
        super().__init__(*group)

        self.frames = ball_frames

        self.cur_frame = 0

        self.vx, self.vy = array_speed

        self.image = self.frames[self.cur_frame]
        if self.vy != 0:
            self.image = pygame.transform.rotate(self.image, -90)
        elif self.vx < 0:
            self.image = pygame.transform.flip(self.image, True, False)

        self.rect = self.image.get_rect().move(pos)
        self.mask = pygame.mask.from_surface(self.image)

        self.update_time_anim = 0
        self.cooldown_anim = 50

        self.attack_power = CONST.ball_attack_power

        self.tiles_group = tiles

        self.person = person
        self.statue = statue

        self.hit = True

        self.hp = 0

    def update(self, surface):
        self.rect.x += self.vx
        self.rect.y += self.vy

        if not -300 <= self.rect.x <= CONST.SCREEN_WIDTH + 300:
            self.kill()

        if pygame.sprite.collide_mask(self, self.person) and not self.person.hit:
            self.person.hp -= self.attack_power
            self.person.hit = True
            self.kill()

        if pygame.sprite.collide_mask(self, self.statue):
            self.statue.hp -= self.attack_power
            self.kill()

        for tiles in self.tiles_group:
            if pygame.sprite.collide_mask(self, tiles):
                self.kill()

        surface.blit(self.image, self.rect)

        # updates the animation for a certain period of time
        if pygame.time.get_ticks() - self.update_time_anim > self.cooldown_anim:
            self.update_sheet()
            self.update_time_anim = pygame.time.get_ticks()

    def update_sheet(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
        self.mask = pygame.mask.from_surface(self.image)

        if self.vy != 0:
            self.image = pygame.transform.rotate(self.image, -90)
        elif self.vx < 0:
            self.image = pygame.transform.flip(self.image, True, False)


class Crystal(pygame.sprite.Sprite):
    def __init__(self, pos, boss, *group):
        super().__init__(*group)

        self.frames = crystal_frames

        self.cur_frame = 0

        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect().move(pos)
        self.mask = pygame.mask.from_surface(self.image)

        self.update_time_anim = 0
        self.cooldown_anim = 100

        self.boss = boss

        self.hit = False
        self.heath_start = self.hp = self.boss.heath_start // 1.5 - self.boss.heath_start // 4

    def update(self, surface):
        if self.hit:
            sword_hit_sound.play()
            self.hit = False

        surface.blit(self.image, self.rect)
        self.draw_heath(surface)

        if self.hp <= 0:
            self.boss.hp -= (self.boss.heath_start // 1.5 - self.boss.heath_start // 4) // 4
            self.kill()

        if pygame.time.get_ticks() - self.update_time_anim > self.cooldown_anim:
            self.update_sheet()
            self.update_time_anim = pygame.time.get_ticks()

    def update_sheet(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
        self.mask = pygame.mask.from_surface(self.image)

    def draw_heath(self, surface):
        coordinates_list = [self.rect.x + self.rect[2] // 2.75, self.rect.y, self.rect[2] * 0.25,
                            5,
                            self.rect.x - 20 + self.rect[2]]

        pygame.draw.rect(surface, (64, 0, 0),
                         (coordinates_list[0], coordinates_list[1], coordinates_list[2], coordinates_list[3]))

        pygame.draw.rect(surface, (0, 128, 0),
                         (coordinates_list[0], coordinates_list[1],
                          coordinates_list[2] * (self.hp / self.heath_start),
                          coordinates_list[3]))


ball_frames = []
crystal_frames = []

portal_sheet = load_image(f'enemy/boss/bullet.png')
crystal_sheet = load_image(f'enemy/boss/crystal.png')

len_sheet = 4

for j in range(len_sheet):
    rect_portal = pygame.Rect(0, 0, portal_sheet.get_width(), portal_sheet.get_height() // len_sheet)

    frame_location_portal = (0, rect_portal.h * j)
    ball_frames.append(portal_sheet.subsurface(pygame.Rect(frame_location_portal, rect_portal.size)))

for j in range(len_sheet):
    rect_crystal = pygame.Rect(0, 0, crystal_sheet.get_width() // len_sheet, crystal_sheet.get_height())

    frame_location_portal = (rect_crystal.w * j, 0)
    crystal_frames.append(crystal_sheet.subsurface(pygame.Rect(frame_location_portal, rect_crystal.size)))

sword_hit_sound = pygame.mixer.Sound('data/music/a blow to the armor.mp3')
boss_sound = pygame.mixer.Sound('data/music/Slide Cinética.mp3')

sword_hit_sound.set_volume(0.1)
boss_sound.set_volume(0.9)
