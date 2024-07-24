import pygame
from .visual import load_image
from scripts import constants as CONST

joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, tiles, enemy_group, *group):
        super().__init__(*group)

        self.frames = []

        self.tiles_sprites = tiles

        self.cut_sheet(CONST.player_sheet_list[self.player_index])

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
        self.ability_anim = False

        self.first_ability_activate = False
        self.time_first_ability = -CONST.update_first_ability

        self.second_ability_activate = False
        self.time_second_ability = -CONST.update_second_ability

        self.back_icon = load_image('playersPanel/Frame.png', transforms=(48, 48))
        self.back_min_icon = load_image('playersPanel/Frame.png', transforms=(16, 16))
        self.preview = load_image('playersPanel/knight.png', transforms=(128, 128))
        self.recharge_icon = load_image('playersPanel/recharge.png', transforms=(40, 40))

        self.font = pygame.font.Font('data/fonts/Stefan Stoychev - Block Light.ttf', 12)
        self.font_money = pygame.font.Font('data/fonts/Stefan Stoychev - Block Light.ttf', 25)

        self.text_button_first_ability = self.font.render('X', False, (255, 255, 255))
        self.text_button_second_ability = self.font.render('C', False, (255, 255, 255))

        self.fon_money = load_image('button/fon_money.png', transforms=(118, 32))
        self.money_icon = load_image('playersPanel/money_icon.png', transforms=(16, 16))
        self.fon_money.set_alpha(200)

        self.joystick = None

    def update(self, surface):
        # If he died
        if self.hp <= 0 and not self.death:
            self.death = True
            self.index = 3
            self.cur_frame = 0

        elif not self.death:
            self.rect.x += self.movement_x
            self.rect.y += self.movement_y

            if self.movement_x == 0:
                sound_walking.stop()

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

            # checking whether the user is standing on the blocks
            if self.rect.y != rect_y:
                self.double_jump = True
                self.jump = False
                self.power_attraction = self.power_jump
                self.movement_y = 1
            else:
                self.movement_y += 0.2

            self.attack_is_complete = self.attack_enemy()

            # if the player has taken damage and the damage animation has not started yet
            if self.hit and self.index != 4:
                self.cur_frame = 0
                self.attack_flag = False
                self.index = 4

                sound_hit.play()

        # if the player goes beyond the boundaries of the world
        if self.rect.x + CONST.TILE_WIDTH * 3 <= 0 or self.rect.x >= CONST.SCREEN_WIDTH - CONST.TILE_WIDTH * 4:
            self.rect.x -= self.movement_x * 1.1

        # displays the player
        surface.blit(self.image, self.rect)
        self.draw_preview(surface)

        # updates the animation for a certain period of time
        if pygame.time.get_ticks() - self.update_time_anim > self.cooldown_anim:
            self.update_sheet()
            self.update_time_anim = pygame.time.get_ticks()

        self.first_ability()
        self.second_ability()

    def events_movement(self, event):
        if not self.death:
            if self.joystick:
                self.events_movement_joystick(event)

            self.events_movement_keyboard(event)

        if event.type == pygame.JOYDEVICEADDED:
            self.joystick = pygame.joystick.Joystick(event.device_index)
            self.text_button_second_ability = self.font.render('Y', False, (255, 255, 255))

        if event.type == pygame.JOYDEVICEREMOVED:
            self.joystick = None
            self.text_button_second_ability = self.font.render('C', False, (255, 255, 255))

    def events_movement_keyboard(self, event):
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
                if not self.jump:
                    sound_walking.stop()
                    sound_walking.play(-1)

            if event.key == pygame.K_a:
                self.movement_x = -self.speed
                self.flip = True
                if not self.attack_flag:
                    self.index = 1
                if not self.jump:
                    sound_walking.stop()
                    sound_walking.play(-1)

            if event.key == pygame.K_LCTRL:
                self.speed *= 1.5
                self.movement_x *= 1.5
                self.cooldown_anim //= 2
                self.attack_power /= 2

            if event.key == pygame.K_x:
                self.first_ability_activate = True

            if event.key == pygame.K_c:
                self.second_ability_activate = True

            # if event.key == pygame.K_l:
            #     for enemy in self.enemy_group:
            #         enemy.kill()
            #
            if event.key == pygame.K_e:
                for enemy in self.enemy_group:
                    print(f'attack:{enemy.attack_power} hp:{enemy.heath_start}')

            if event.key == pygame.K_SPACE:
                if self.power_attraction <= 10 and self.double_jump:
                    self.power_attraction = self.power_jump
                    self.double_jump = False

                    sound_jump.play()
                if not self.jump:
                    self.jump = True

                    sound_jump.play()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.attack_flag = True
                self.cur_frame = 0
                self.index = 2

            elif event.button == 3:
                self.first_ability_activate = True

    def events_movement_joystick(self, event):
        if event.type == 1536 or event.type == 1538:
            hats = self.joystick.get_numhats()

            for i in range(hats):
                if not self.joystick.get_axis(0) == 0:
                    self.movement_x = self.speed * self.joystick.get_axis(0)
                else:
                    self.movement_x = self.speed * self.joystick.get_hat(i)[0]

                if not self.attack_flag and not self.hit:
                    self.index = 1

                if self.movement_x < 0:
                    self.flip = True

                elif self.movement_x > 0:
                    self.flip = False

                elif not self.attack_flag and not self.hit:
                    self.index = 0
                    sound_walking.stop()

                if self.joystick.get_hat(i)[1] != 0 or self.joystick.get_axis(1) == -1.0:
                    if self.power_attraction <= 10 and self.double_jump:
                        self.power_attraction = self.power_jump
                        self.double_jump = False

                        sound_jump.play()

                    if not self.jump:
                        self.jump = True

                        sound_jump.play()

        if event.type == pygame.JOYBUTTONUP:
            if event.button == 0:
                self.speed //= 1.5
                self.movement_x //= 1.5
                self.cooldown_anim *= 2
                self.attack_power *= 2

            elif event.button == 1:
                self.attack_flag = True
                self.cur_frame = 0
                self.index = 2

            elif event.button == 2:
                self.first_ability_activate = True

            elif event.button == 3:
                self.second_ability_activate = True

        elif event.type == pygame.JOYBUTTONDOWN:
            if event.button == 0:
                self.speed *= 1.5
                self.movement_x *= 1.5
                self.cooldown_anim //= 2
                self.attack_power /= 2

        if (self.joystick.get_axis(5) > 0.98 or self.joystick.get_axis(4) > 0.98) and not self.attack_flag:
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

            # if the ability has ended
            elif self.ability_anim:
                self.ability_anim = False

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

        # if the animation has come to the moment of impact
        if self.attack_flag and self.cur_frame > 3 and not self.attack_is_complete:

            if self.cur_frame == 4 and pygame.time.get_ticks() - self.update_time_anim >= self.cooldown_anim:
                sound_attack.play()

            for sprite in self.enemy_group:
                if pygame.sprite.collide_mask(self, sprite) and not sprite.hit:
                    sprite.hp -= self.attack_power
                    flag = sprite.hit = True
        return flag

    def draw_preview(self, surface):
        surface.blit(self.preview, (10, 10))
        pygame.draw.rect(surface, (0, 0, 0), (0, 0, 138, 138), 10)

        size_cell = (10 * self.heath_start if self.heath_start <= 33 else 330, 128)
        cell_of_lives = load_image('playersPanel/TheCellOfLives.png', transforms=size_cell)

        coordinates_list = [165, 25, size_cell[0] // 1.6, size_cell[1] - 115, 150 + size_cell[0]]

        pygame.draw.rect(surface, (64, 0, 0),
                         (coordinates_list[0], coordinates_list[1], coordinates_list[2],
                          coordinates_list[3]))

        pygame.draw.rect(surface, (0, 64, 0),
                         (coordinates_list[0], coordinates_list[1],
                          coordinates_list[2] * (self.hp / self.heath_start),
                          coordinates_list[3]))

        surface.blit(cell_of_lives, (coordinates_list[0] - self.heath_start * 0.4, coordinates_list[1] - 95))

        surface.blit(self.back_icon, (coordinates_list[0], coordinates_list[1] * 2.5))
        surface.blit(self.back_icon, (coordinates_list[2] - 40 + coordinates_list[0], coordinates_list[1] * 2.5))

        surface.blit(self.back_min_icon, (coordinates_list[0] * 1.1, coordinates_list[1] * 2.5 * 1.65))
        surface.blit(self.back_min_icon,
                     ((coordinates_list[2] - 40 + coordinates_list[0]) * 1.06, coordinates_list[1] * 2.5 * 1.65))

        surface.blit(self.text_button_first_ability,
                     (coordinates_list[0] * 1.135, coordinates_list[1] * 2.5 * 1.65 - 2))
        surface.blit(self.text_button_second_ability, ((coordinates_list[2] - 40 + coordinates_list[0]) * 1.08,
                                                       coordinates_list[1] * 2.5 * 1.65 - 2))

        pygame.draw.rect(surface, (0, 0, 0),
                         (coordinates_list[0] + 45, coordinates_list[1] * 3.2, coordinates_list[2] - 83, 10))

        surface.blit(self.first_icon_ability, (coordinates_list[0] + 4, coordinates_list[1] * 2.5 + 4))
        surface.blit(self.second_icon_ability,

                     (coordinates_list[2] - 36 + coordinates_list[0], coordinates_list[1] * 2.5 + 4))

        money_text = self.font_money.render(str(CONST.money), False, (0, 0, 0))

        surface.blit(self.fon_money, (10, 140))
        surface.blit(self.money_icon, (15, 148))

        surface.blit(money_text, (80 - len(str(CONST.money)) * 5, 137.5))

        text_heath = self.font.render(f'heath_full: {self.heath_start}', False, (0, 0, 0))
        text_attack = self.font.render(f'attack power: {self.attack_power}', False, (0, 0, 0))

        surface.blit(text_heath, (0, 150))
        surface.blit(text_attack, (0, 165))


def is_collided_with(sprite_person, sprite_group):
    for sprite in sprite_group:
        if pygame.sprite.collide_mask(sprite_person, sprite):
            return sprite
    return False


sound_jump = pygame.mixer.Sound('data/music/jump_sound.mp3')
sound_walking = pygame.mixer.Sound('data/music/hodbyi.mp3')
sound_attack = pygame.mixer.Sound('data/music/zvuk-byistrogo-vzmaha-mecha.mp3')
sound_hit = pygame.mixer.Sound('data/music/taking damage by a human.mp3')

sound_jump.set_volume(0.5)
