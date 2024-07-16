import pygame
from scripts.players import Player
from scripts import constants as CONST
from scripts.visual import load_image


class Knight(Player):
    def __init__(self, pos, tiles, enemy_group, *group):
        self.player_index = 0

        super().__init__(pos, tiles, enemy_group, *group)

        self.speed = CONST.knight_speed

        self.power_jump = CONST.knight_power_jump

        self.attack_power = CONST.knight_attack_power

        self.cooldown_anim = CONST.knight_cooldown_anim

        self.heath_start = self.hp = CONST.knight_heath

        self.first_ability_activate = False
        self.time_first_ability = -CONST.update_first_ability

        self.second_ability_activate = False
        self.time_second_ability = -CONST.update_second_ability

        self.first_icon_ability = load_image('playersPanel/knight_skill_first.png', transforms=(40, 40))
        self.second_icon_ability = load_image('playersPanel/knight_skill_second.png', transforms=(40, 40))

    def first_ability(self):
        if pygame.time.get_ticks() - self.time_first_ability >= CONST.update_first_ability:
            self.first_icon_ability = load_image('playersPanel/knight_skill_first.png', transforms=(40, 40))
            if self.first_ability_activate:
                self.time_first_ability = pygame.time.get_ticks()
        else:
            self.first_icon_ability = self.recharge_icon
            self.first_ability_activate = False

    def second_ability(self):
        if pygame.time.get_ticks() - self.time_second_ability >= CONST.update_second_ability:
            self.second_icon_ability = load_image('playersPanel/knight_skill_second.png', transforms=(40, 40))
            if self.second_ability_activate:
                self.hit = True
                self.hp -= self.heath_start // 2

                for enemy in self.enemy_group:
                    enemy.hp -= self.heath_start // 2

                    enemy.hit = True
                    enemy.index = 4

                self.time_second_ability = pygame.time.get_ticks()

                self.second_ability_activate = False
        else:
            self.second_icon_ability = self.recharge_icon
            self.second_ability_activate = False


class Alexander(Player):
    def __init__(self, pos, tiles, enemy_group, *group):
        self.player_index = 1

        super().__init__(pos, tiles, enemy_group, *group)

        self.speed = CONST.alexander_speed

        self.power_jump = CONST.alexander_power_jump

        self.attack_power = CONST.alexander_attack_power

        self.cooldown_anim = CONST.alexander_cooldown_anim

        self.heath_start = self.hp = CONST.alexander_heath

        self.first_ability_activate = False
        self.time_first_ability = -CONST.alexander_update_first_ability

        self.second_ability_activate = False
        self.time_second_ability = -CONST.alexander_update_second_ability

        self.preview = load_image('playersPanel/alexander.png', transforms=(128, 128))

        self.first_icon_ability = load_image('playersPanel/alexander_skill_first.png', transforms=(40, 40))
        self.second_icon_ability = load_image('playersPanel/alexander_skill_second.png', transforms=(40, 40))

    def attack_enemy(self):
        # returns the truth if there is an enemy nearby
        flag = False

        # if the animation has come to the moment of impact
        if self.attack_flag and not (self.cur_frame < 3 or 5 <= self.cur_frame <= 6) and not self.attack_is_complete:
            for sprite in self.enemy_group:
                if pygame.sprite.collide_mask(self, sprite) and not sprite.hit:
                    sprite.hp -= self.attack_power
                    flag = sprite.hit = True
        elif self.attack_flag and self.cur_frame == 6 and self.attack_is_complete:
            flag = False

        return flag

    def first_ability(self):
        if pygame.time.get_ticks() - self.time_first_ability >= CONST.update_first_ability:
            self.first_icon_ability = load_image('playersPanel/alexander_skill_first.png', transforms=(40, 40))
            if self.first_ability_activate:
                self.hp = self.heath_start

                self.index = 5
                self.ability_anim = False

                self.first_ability_activate = False

                self.time_first_ability = pygame.time.get_ticks()
        else:
            self.first_icon_ability = self.recharge_icon
            self.first_ability_activate = False

    def second_ability(self):
        if pygame.time.get_ticks() - self.time_second_ability >= CONST.update_second_ability:
            self.second_icon_ability = load_image('playersPanel/alexander_skill_second.png', transforms=(40, 40))
            if self.second_ability_activate:
                Sword((CONST.SCREEN_WIDTH + 100, 550), self.enemy_group, (-20, 0), self.attack_power,
                      self.enemy_group)
                Sword((-100, 575), self.enemy_group, (20, 0), self.attack_power,
                      self.enemy_group)
                Sword((CONST.SCREEN_WIDTH // 2 + 50, CONST.SCREEN_HEIGHT + 100), self.enemy_group, (0, 20),
                      self.attack_power,
                      self.enemy_group)
                Sword((CONST.SCREEN_WIDTH // 2 - 100, -100), self.enemy_group, (0, -20), self.attack_power,
                      self.enemy_group)

                self.second_ability_activate = False
                self.time_second_ability = pygame.time.get_ticks()
        else:
            self.second_icon_ability = self.recharge_icon
            self.second_ability_activate = False


class Samurai(Player):
    def __init__(self, pos, tiles, enemy_group, *group):
        self.player_index = 2

        super().__init__(pos, tiles, enemy_group, *group)

        self.speed = CONST.samurai_speed

        self.power_jump = CONST.samurai_power_jump

        self.attack_power = CONST.samurai_attack_power

        self.cooldown_anim = CONST.samurai_cooldown_anim

        self.heath_start = self.hp = CONST.samurai_heath

        self.first_ability_activate = False
        self.time_first_ability = -CONST.samurai_update_first_ability

        self.second_ability_activate = False
        self.time_second_ability = -CONST.samurai_update_second_ability

        self.preview = load_image('playersPanel/samurai.png', transforms=(128, 128))

        self.first_icon_ability = load_image('playersPanel/samurai_skill_first.png', transforms=(40, 40))
        self.second_icon_ability = load_image('playersPanel/samurai_skill_second.png', transforms=(40, 40))

    def attack_enemy(self):
        # returns the truth if there is an enemy nearby
        flag = False

        # if the animation has come to the moment of impact
        if self.attack_flag and not (self.cur_frame < 4 or 6 <= self.cur_frame <= 9) and not self.attack_is_complete:
            for sprite in self.enemy_group:
                if pygame.sprite.collide_mask(self, sprite) and not sprite.hit:
                    sprite.hp -= self.attack_power
                    flag = sprite.hit = True
        elif self.attack_flag and self.cur_frame == 9 and self.attack_is_complete:
            flag = False

        return flag

    def first_ability(self):
        if pygame.time.get_ticks() - self.time_first_ability >= CONST.update_first_ability:
            self.first_icon_ability = load_image('playersPanel/samurai_skill_first.png', transforms=(40, 40))
            if self.first_ability_activate:
                if self.rect.y >= 350:
                    self.rect.y = 250
                else:
                    self.rect.y = 500

                self.first_ability_activate = False
                self.time_first_ability = pygame.time.get_ticks()
        else:
            self.first_icon_ability = self.recharge_icon
            self.first_ability_activate = False

    def second_ability(self):
        if pygame.time.get_ticks() - self.time_second_ability >= CONST.update_second_ability:
            self.second_icon_ability = load_image('playersPanel/samurai_skill_second.png', transforms=(40, 40))
            if self.second_ability_activate:
                Wolf(self.enemy_group, self.attack_power, self.enemy_group)

                self.second_ability_activate = False
                self.time_second_ability = pygame.time.get_ticks()
        else:
            self.second_icon_ability = self.recharge_icon
            self.second_ability_activate = False


class Sword(pygame.sprite.Sprite):
    def __init__(self, pos, enemy_group, array_speed, attack_power, *group):
        super().__init__(*group)

        self.image = load_image('players/player_alexander/sword.png')
        self.image.get_rect().move(pos)

        self.vx, self.vy = array_speed

        if self.vy > 0:
            self.image = pygame.transform.rotate(self.image, 45)
        elif self.vx > 0:
            self.image = pygame.transform.rotate(self.image, -45)
        elif self.vy < 0:
            self.image = pygame.transform.rotate(self.image, -135)
        else:
            self.image = pygame.transform.rotate(self.image, -225)

        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect().move(pos)

        self.attack_power = attack_power

        self.enemy_group = enemy_group

        self.hit = True

    def update(self, surface):
        if not -300 < self.rect.x < CONST.SCREEN_WIDTH + 300 or not -300 < self.rect.y < CONST.SCREEN_HEIGHT + 300:
            self.kill()

        for sprite in self.enemy_group:
            if pygame.sprite.collide_mask(self, sprite) and not sprite.hit:
                sprite.hp -= self.attack_power
                sprite.hit = True

        self.rect.x += self.vx
        self.rect.y -= self.vy

        surface.blit(self.image, self.rect)


class Wolf(pygame.sprite.Sprite):
    def __init__(self, enemy_group, attack_power, *group):
        super().__init__(*group)

        self.frames = wolf_frames

        self.cur_frame = 0
        self.index = 1

        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect().move((CONST.SCREEN_WIDTH + 300, 450))

        self.mask = pygame.mask.from_surface(self.image)

        self.update_time_anim = 0
        self.cooldown_anim = 75

        self.attack_power = attack_power // 2

        self.enemy_group = enemy_group

        self.hit = True

    def update(self, surface):
        self.rect.x -= 15

        for sprite in self.enemy_group:
            if pygame.sprite.collide_mask(self, sprite) and not sprite.hit:
                sprite.hp -= self.attack_power
                sprite.hit = True

        surface.blit(self.image, self.rect)

        # updates the animation for a certain period of time
        if pygame.time.get_ticks() - self.update_time_anim > self.cooldown_anim:
            self.update_sheet()
            self.update_time_anim = pygame.time.get_ticks()

        if self.rect.x <= -100:
            self.kill()

    def update_sheet(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
        self.mask = pygame.mask.from_surface(self.image)


wolf_frames = []

wolf_sheet = load_image(f'enemy/wolf.png')
len_sheet = 5

for j in range(len_sheet):
    rect_wolf = pygame.Rect(0, 0, wolf_sheet.get_width() // len_sheet, wolf_sheet.get_height())

    frame_location_wolf = (rect_wolf.w * j, 0)
    wolf_frames.append(wolf_sheet.subsurface(pygame.Rect(frame_location_wolf, rect_wolf.size)))
