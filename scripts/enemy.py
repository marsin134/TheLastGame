import pygame
from math import sqrt
from .visual import load_image
from .players import is_collided_with
from scripts import constants as CONST


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, tiles, person, statue, *group):
        super().__init__(*group)

        self.frames = []

        self.tiles_sprites = tiles

        self.cut_sheet(CONST.enemy_specifications[self.enemy_index]['list_sheet'])

        self.cur_frame = 0
        self.index = 1

        self.image = self.frames[0][self.cur_frame]
        self.rect = self.image.get_rect().move(pos)

        self.vx, self.vy = CONST.enemy_specifications[self.enemy_index]['speed'], 5

        self.update_time_anim = pygame.time.get_ticks()
        self.cooldown_anim = CONST.enemy_specifications[self.enemy_index]['anim']

        self.flip = False

        self.person = person
        self.statue = statue

        self.purpose = statue

        self.mask = pygame.mask.from_surface(self.image)

        self.range_player = CONST.enemy_specifications[self.enemy_index]['range']

        self.attack_flag = False
        self.attack_is_complete = False
        self.attack_power = CONST.enemy_specifications[self.enemy_index]['attack']

        self.heath_start = self.hp = CONST.enemy_specifications[self.enemy_index]['heath']

        self.hit = False
        self.death = False

    def cut_sheet(self, list_sheet):
        sheet = load_image(f'enemy/{list_sheet[0][0]}')
        self.rect = pygame.Rect(0, 0, sheet.get_width() // list_sheet[0][1], sheet.get_height())

        for i in range(len(list_sheet)):
            sheet = load_image(f'enemy/{list_sheet[i][0]}')
            frame_list = []
            for j in range(list_sheet[i][1]):
                self.rect = pygame.Rect(0, 0, sheet.get_width() // list_sheet[i][1], sheet.get_height())

                frame_location = (self.rect.w * j, 0)
                frame_list.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))
            self.frames.append(frame_list)

    def update_sheet(self):
        # if the animation is over
        if (self.cur_frame + 1) % len(self.frames[self.index]) == 0:
            if self.death:
                self.kill()

            # if the hit has ended
            elif self.hit:
                self.hit = False

            # if the attack has ended
            elif self.attack_flag and (self.cur_frame + 1) % len(self.frames[self.index]) == 0:
                self.attack_flag = False
                self.attack_is_complete = False

        self.cur_frame = (self.cur_frame + 1) % len(self.frames[self.index])
        self.image = self.frames[self.index][self.cur_frame]
        if self.flip:
            self.image = pygame.transform.flip(self.image, True, False)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, surface):
        if self.hp <= 0 and not self.death:
            self.death = True
            self.index = 3
            self.cur_frame = 0
            self.cooldown_anim = 200

        elif not self.death:
            # attacks the player
            if (self.attack_flag and self.cur_frame > 5 and not self.attack_is_complete
                    and pygame.sprite.collide_mask(self, self.purpose) and not self.purpose.hit):
                self.purpose.hp -= self.attack_power
                self.purpose.hit = True
                self.attack_is_complete = True

            # if the target is alive
            if self.purpose.hp > 0:
                # returns to the standard settings
                if not self.attack_flag and not self.hit:
                    self.index = 1
                    self.vx = CONST.enemy_specifications[self.enemy_index]['speed']

                # they will determine how to move towards the goal
                self.moving_towards_the_goal()
            else:
                self.index = 0

            self.pick_target()

            # if it concerns the blocks, then we raise
            if is_collided_with(self, self.tiles_sprites):
                self.rect.y -= self.vy

            self.checking_events_with_the_player()
            self.rect.y += self.vy

        # displays the player
        surface.blit(self.image, self.rect)
        self.draw_heath(surface)

        # updates the animation for a certain period of time
        if pygame.time.get_ticks() - self.update_time_anim > self.cooldown_anim:
            self.update_sheet()
            self.update_time_anim = pygame.time.get_ticks()

    def pick_target(self):
        # defines the goal
        x_dist = self.person.rect.x - self.rect.x
        y_dist = self.person.rect.y - self.rect.y
        dist = sqrt(x_dist ** 2 + y_dist ** 2)
        if dist < self.range_player and self.rect.y <= self.person.rect.y + CONST.TILE_HEIGHT * 2:
            self.purpose = self.person
        elif self.statue.hp > 0:
            self.purpose = self.statue

    def draw_heath(self, surface):
        coordinates_list = [self.rect.x + self.rect[2] // 2.5, self.rect.y + self.rect[3] // 2.8, self.rect[2] * 0.25,
                            5,
                            self.rect.x - 20 + self.rect[2]]

        pygame.draw.rect(surface, (64, 0, 0),
                         (coordinates_list[0], coordinates_list[1], coordinates_list[2], coordinates_list[3]))

        pygame.draw.rect(surface, (0, 128, 0),
                         (coordinates_list[0], coordinates_list[1],
                          coordinates_list[2] * (self.hp / self.heath_start),
                          coordinates_list[3]))

    def checking_events_with_the_player(self):
        if pygame.sprite.collide_mask(self, self.purpose):
            # if the player has taken damage and the damage animation has not started yet
            if self.hit and self.index != 4:
                self.attack_flag = False
                self.index = 4
                self.cur_frame = 0

                self.vx = 0

            # if the animation has come to the moment of impact
            elif not self.attack_flag and not self.hit:
                self.attack_flag = True

                self.index = 2
                self.cur_frame = 0

                self.vx = 0

    def moving_towards_the_goal(self):
        if self.rect.x < self.purpose.rect.x:
            self.rect.x += self.vx
            self.flip = False

        else:
            self.rect.x -= self.vx
            self.flip = True


class Goblin(Enemy):
    def __init__(self, pos, tiles, person, statue, *group):
        self.enemy_index = 0
        super().__init__(pos, tiles, person, statue, *group)


class Skeleton(Enemy):
    def __init__(self, pos, tiles, person, statue, *group):
        self.enemy_index = 1
        super().__init__(pos, tiles, person, statue, *group)

    def draw_heath(self, surface):
        coordinates_list = [self.rect.x + self.rect[2] // 2.5, self.rect.y + self.rect[3] // 3.5, self.rect[2] * 0.25,
                            5,
                            self.rect.x - 20 + self.rect[2]]

        pygame.draw.rect(surface, (64, 0, 0),
                         (coordinates_list[0], coordinates_list[1], coordinates_list[2], coordinates_list[3]))

        pygame.draw.rect(surface, (0, 128, 0),
                         (coordinates_list[0], coordinates_list[1],
                          coordinates_list[2] * (self.hp / self.heath_start),
                          coordinates_list[3]))


class FlyingEye(Enemy):
    def __init__(self, pos, tiles, person, statue, *group):
        self.enemy_index = 2
        super().__init__(pos, tiles, person, statue, *group)
        self.vy = 1

    def pick_target(self):
        # defines the goal
        self.purpose = self.statue

    def checking_events_with_the_player(self):
        if pygame.sprite.collide_mask(self, self.purpose):
            # if the animation has come to the moment of impact
            if not self.attack_flag and not self.hit:
                self.attack_flag = True

                self.index = 2
                self.cur_frame = 0

                self.vx = 0
                self.vy = 0

        if pygame.sprite.collide_mask(self, self.person):
            if self.hit and self.index != 4:
                self.attack_flag = False
                self.index = 4
                self.cur_frame = 0

                self.vx = 0

    def moving_towards_the_goal(self):
        if self.rect.x < self.purpose.rect.x:
            self.rect.x += self.vx
            if not pygame.sprite.collide_circle(self, self.purpose):
                self.flip = False
            else:
                self.vy = 5
        else:
            self.rect.x -= self.vx
            if not pygame.sprite.collide_circle(self, self.purpose):
                self.flip = True
            else:
                self.vy = 5


class Mushroom(Enemy):
    def __init__(self, pos, tiles, person, statue, *group):
        self.enemy_index = 3
        super().__init__(pos, tiles, person, statue, *group)

    def pick_target(self):
        # defines the goal
        self.purpose = self.person

    def moving_towards_the_goal(self):
        if not (self.purpose.rect.x - 1 <= self.rect.x <= self.purpose.rect.x + 1
                and self.rect.y > self.purpose.rect.y):
            if self.rect.x < self.purpose.rect.x:
                self.rect.x += self.vx
                self.flip = False
            else:
                self.rect.x -= self.vx
                self.flip = True
        else:
            self.index = 0