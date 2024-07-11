import pygame
from .visual import load_image
from scripts import constants as CONST


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, tiles, enemy_group, *group):
        super().__init__(*group)

        self.frames = []

        self.tiles_sprites = tiles

        self.cut_sheet([('player_knight/IDLE.png', 3),
                        ('player_knight/WALK.png', 8),
                        ('player_knight/ATTACK.png', 7),
                        ('player_knight/DEATH.png', 10),
                        ('player_knight/HURT.png', 3)])

        self.preview = load_image('playersPanel/knight.png', transforms=(128, 128))

        self.cur_frame = 0
        self.index = 0

        self.image = self.frames[0][self.cur_frame]
        self.rect = self.image.get_rect().move(pos)

        self.enemy_group = enemy_group

        self.movement_x = 0
        self.movement_y = 1

        self.speed = 0

        self.flip = False

        self.jump = False
        self.double_jump = True
        self.power_jump = 0
        self.power_attraction = self.power_jump

        self.attack_flag = False
        self.attack_is_complete = False
        self.attack_power = 0

        self.mask = pygame.mask.from_surface(self.image)

        self.update_time_anim = pygame.time.get_ticks()
        self.cooldown_anim = 0

        self.heath_start = self.hp = CONST.knight_heath

        self.hit = False
        self.death = False

    def update(self, surface):
        # If he died
        if self.hp <= 0 and not self.death:
            self.death = True
            self.index = 3
            self.cur_frame = 0

        elif not self.death:
            self.rect.x += self.movement_x
            self.rect.y += self.movement_y

            # increasing the force of gravity
            if self.jump and not self.hit:
                self.rect.y -= self.power_attraction
                self.power_attraction -= 1
                if self.power_attraction <= 0:
                    self.power_attraction = 0

            # y coordinates when gravity was triggered
            rect_y = self.rect.y

            # if it concerns the blocks, then we raise
            if is_collided_with(self, self.tiles_sprites):
                self.rect.y -= self.movement_y

            # if the player goes beyond the boundaries of the world
            if self.rect.x + CONST.TILE_WIDTH * 2 <= 0 or self.rect.x >= CONST.SCREEN_WIDTH - CONST.TILE_WIDTH * 3.5:
                self.movement_x -= self.movement_x

            # checking whether the user is standing on the blocks
            if self.rect.y != rect_y:
                self.double_jump = True
                self.jump = False
                self.power_attraction = self.power_jump
                self.movement_y = 1
            else:
                self.movement_y += 0.2

            # if the animation has come to the moment of impact
            if self.attack_flag and self.cur_frame > 3 and not self.attack_is_complete:
                self.attack_is_complete = self.attack_enemy()

            # if the player has taken damage and the damage animation has not started yet
            if self.hit and self.index != 4:
                self.cur_frame = 0
                self.attack_flag = False
                self.index = 4

        # displays the player
        surface.blit(self.image, self.rect)
        self.draw_preview(surface)

        # updates the animation for a certain period of time
        if pygame.time.get_ticks() - self.update_time_anim > self.cooldown_anim:
            self.update_sheet()
            self.update_time_anim = pygame.time.get_ticks()

    def events_movement(self, event):
        if not self.death:
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_d and not pygame.key.get_pressed()[pygame.K_a]:
                    self.movement_x = 0
                    if not self.attack_flag:
                        self.index = 0

                if event.key == pygame.K_a and not pygame.key.get_pressed()[pygame.K_d]:
                    self.movement_x = 0
                    if not self.attack_flag:
                        self.index = 0

                if event.key == pygame.K_LCTRL:
                    self.speed //= 1.5
                    self.movement_x //= 1.5
                    self.cooldown_anim *= 2
                    self.attack_power *= 2

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    self.movement_x = self.speed
                    self.flip = False
                    if not self.attack_flag:
                        self.index = 1

                if event.key == pygame.K_a:
                    self.movement_x = -self.speed
                    self.flip = True
                    if not self.attack_flag:
                        self.index = 1

                if event.key == pygame.K_LCTRL:
                    self.speed *= 1.5
                    self.movement_x *= 1.5
                    self.cooldown_anim //= 2
                    self.attack_power /= 2

                if event.key == pygame.K_SPACE:
                    if self.power_attraction <= 10 and self.double_jump:
                        self.power_attraction = self.power_jump
                        self.double_jump = False
                    if not self.jump:
                        self.jump = True

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.attack_flag = True
                self.cur_frame = 0
                self.index = 2

    def cut_sheet(self, list_sheet):
        # creating sprites
        sheet = load_image(f'players/{list_sheet[0][0]}')
        self.rect = pygame.Rect(0, 0, sheet.get_width() // list_sheet[0][1], sheet.get_height())

        for i in range(len(list_sheet)):
            sheet = load_image(f'players/{list_sheet[i][0]}')
            frame_list = []
            for j in range(list_sheet[i][1]):
                self.rect = pygame.Rect(0, 0, sheet.get_width() // list_sheet[i][1], sheet.get_height())

                frame_location = (self.rect.w * j, 0)
                frame_list.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))
            self.frames.append(frame_list)

    def update_sheet(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames[self.index])
        self.image = self.frames[self.index][self.cur_frame]
        if self.flip:
            self.image = pygame.transform.flip(self.image, True, False)
        self.mask = pygame.mask.from_surface(self.image)

        # if the animation is over
        if (self.cur_frame + 1) % len(self.frames[self.index]) == 0:
            if self.death:
                self.kill()

            # if the hit has ended
            elif self.hit:
                self.hit = False

            # if the attack has ended
            elif self.attack_flag:
                self.attack_flag = False
                self.attack_is_complete = False

            self.index = 0
            if self.movement_x != 0:
                self.index = 1

    def attack_enemy(self):
        # returns the truth if there is an enemy nearby
        flag = False
        for sprite in self.enemy_group:
            if pygame.sprite.collide_mask(self, sprite) and not sprite.hit:
                sprite.hp -= self.attack_power
                flag = sprite.hit = True
        return flag

    def draw_preview(self, surface):
        surface.blit(self.preview, (10, 10))
        pygame.draw.rect(surface, (0, 0, 0), (0, 0, 138, 138), 10)

        coordinates_list = [165, 25, size_cell[0] // 1.6, size_cell[1] - 115, 150 + size_cell[0]]

        pygame.draw.rect(surface, (64, 0, 0),
                         (coordinates_list[0], coordinates_list[1], coordinates_list[2],
                          coordinates_list[3]))

        pygame.draw.rect(surface, (0, 64, 0),
                         (coordinates_list[0], coordinates_list[1],
                          coordinates_list[2] * (self.hp / self.heath_start),
                          coordinates_list[3]))

        surface.blit(cell_of_lives, (coordinates_list[0] - 15, coordinates_list[1] - 95))


class Knight(Player):
    def __init__(self, pos, tiles, enemy_group, *group):
        super().__init__(pos, tiles, enemy_group, *group)
        self.speed = CONST.knight_speed

        self.power_jump = CONST.knight_power_jump

        self.attack_power = CONST.knight_attack_power

        self.cooldown_anim = CONST.knight_cooldown_anim

        self.heath_start = self.hp = CONST.knight_heath


def is_collided_with(sprite_person, sprite_group):
    for sprite in sprite_group:
        if pygame.sprite.collide_mask(sprite_person, sprite):
            return sprite
    return False


size_cell = (256, 128)
cell_of_lives = load_image('playersPanel/TheCellOfLives.png', transforms=size_cell)
