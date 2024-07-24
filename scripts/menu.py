import pygame
from scripts import visual
from scripts import constants as CONST

# create fonts
size_font = 45
font_big = pygame.font.Font('data/fonts/Stefan Stoychev - Block Light.ttf', size_font + 75)
font = pygame.font.Font('data/fonts/Stefan Stoychev - Block Light.ttf', size_font)
font_reduced = pygame.font.Font('data/fonts/Stefan Stoychev - Block Light.ttf', size_font - 2)
font_min = pygame.font.Font('data/fonts/Stefan Stoychev - Block Light.ttf', size_font - 4)
font_pause_min = pygame.font.Font('data/fonts/Stefan Stoychev - Block Light.ttf', size_font - 6)


class Button(pygame.sprite.Sprite):
    def __init__(self, pos, text, image_button, shift, font_normal=font.render,
                 font_min_text=font_reduced.render, color='black'):

        pygame.sprite.Sprite.__init__(self)

        self.image = image_button
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

        self.text = [font_normal(text, 1, pygame.Color(color)),
                     font_min_text(text, 1, pygame.Color(color))]
        self.shift = shift
        self.hovered = False

    def update(self, surface):
        surface.blit(self.image, self.rect)
        if self.rect.collidepoint(pygame.mouse.get_pos()) and not self.hovered:
            self.hovered = True
            music_hooked.play()
        elif not self.rect.collidepoint(pygame.mouse.get_pos()):
            self.hovered = False

        if self.hovered:
            surface.blit(self.text[1], (self.rect.x + self.shift[0], self.rect.y + self.shift[1]))
        else:
            surface.blit(self.text[0], (self.rect.x + self.shift[0], self.rect.y + self.shift[1]))


def menu(surface):
    music_fon_menu.play(-1)

    running = True
    while running:
        for event in pygame.event.get():
            # when closing the window
            if event.type == pygame.QUIT:
                overwrite_money_in_text_files()
                running = False

            if event.type == pygame.MOUSEBUTTONUP:
                # if you click on the start button, we start the game
                if start.rect.collidepoint(event.pos):
                    music_click.play()
                    return True

                # if you click on the exit button, we end the game
                elif exit_in_menu.rect.collidepoint(event.pos):
                    overwrite_money_in_text_files()
                    return False

                # if you click on the button, then open the store
                elif shop_button.rect.collidepoint(event.pos):
                    music_click.play()
                    shop(surface)
        # show fon
        surface.blit(fon, (0, 0))

        # show button
        button_group_menu.update(surface)
        surface.blit(name_game_text, (CONST.SCREEN_WIDTH // 4.5, 100))

        pygame.display.flip()


def shop(surface):
    color_line = (0, 0, 0)
    size_line = 10

    running = True
    while running:
        for event in pygame.event.get():
            # when closing the window
            if event.type == pygame.QUIT:
                overwrite_money_in_text_files()
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONUP:
                if exit_from_shop.rect.collidepoint(event.pos):
                    music_click.play()
                    running = False
                if button_easy.rect.collidepoint(event.pos):
                    music_click.play()
                    overwrite_difficulty_in_text_files(1)
                if button_normal.rect.collidepoint(event.pos):
                    music_click.play()
                    overwrite_difficulty_in_text_files(2.5)
                if button_hard.rect.collidepoint(event.pos):
                    music_click.play()
                    overwrite_difficulty_in_text_files(5)
                if button_knight.rect.collidepoint(event.pos):
                    music_click.play()
                    overwrite_character_in_text_files(0)
                if button_samurai.rect.collidepoint(event.pos):
                    if is_it_possible_to_use_a_character(1):
                        music_click.play()
                        overwrite_character_in_text_files(1)
                if button_alexandr.rect.collidepoint(event.pos):
                    if is_it_possible_to_use_a_character(2):
                        music_click.play()
                        overwrite_character_in_text_files(2)

        surface.blit(fon_shop, (0, 0))

        # draw lines
        pygame.draw.rect(surface, color_line,
                         (size_button[0] + size_line * 2, CONST.SCREEN_HEIGHT // 1.5,
                          CONST.SCREEN_WIDTH - size_button[0] + size_line * 2, size_line))  # horizontal line
        pygame.draw.rect(surface, color_line,
                         (size_button[0] + size_line * 2, 0, size_line, CONST.SCREEN_HEIGHT))  # vertical line

        # shop text blit
        surface.blit(shop_text, ((size_button[0] + size_line) // 2 - (shop_text.get_width() // 2), 0))

        # characters user blit
        icon_user_character = int(open('data/txt_files/saves.txt', 'r', encoding='utf-8').readlines()[2].split()[-1])
        rect_icon = (size_button[0] - size_line * 2, size_button[0] // 1.5 - size_line * 4)
        pos_icon_character = (size_line * 2, 175)
        surface.blit(visual.load_image(dict_characters[icon_user_character], transforms=rect_icon),
                     pos_icon_character)

        # blit frame
        pygame.draw.rect(surface, (0, 0, 0),
                         (pos_icon_character[0], pos_icon_character[1],
                          rect_icon[0] + size_line, rect_icon[1] + size_line), size_line)
        # blit text
        surface.blit(character_user,
                     (size_button[0] // 2 - character_user.get_width() // 2 + size_line * 2,
                      pos_icon_character[1] + rect_icon[1] - size_line))

        # difficulty blit
        surface.blit(image_difficulty, (size_button[0] // 2 - image_difficulty.get_width() // 2 + size_line,
                                        pos_icon_character[1] + rect_icon[1] + 100))
        surface.blit(difficulty_text,
                     ((size_button[0] // 2 - image_difficulty.get_width() // 2 + image_difficulty.get_width() // 3,
                       pos_icon_character[1] + rect_icon[1] + 100 + image_difficulty.get_height())))

        difficulty_array = dict_difficulty[
            float(open('data/txt_files/saves.txt', 'r', encoding='utf-8').readlines()[1].split()[-1])]
        text_difficulty = font_min.render(difficulty_array[0], False, difficulty_array[1])
        rect_x_text_difficulty = size_button[0] - (
                image_difficulty.get_width() - text_difficulty.get_width()) // 2 - text_difficulty.get_width()
        surface.blit(text_difficulty, (rect_x_text_difficulty, pos_icon_character[1] + rect_icon[1] + 105))

        # money blit

        money_text = font_min.render(str(CONST.money), False, (0, 0, 0))

        surface.blit(fon_money, (CONST.SCREEN_WIDTH - fon_money.get_width() - size_line, size_line))
        surface.blit(money_icon, (CONST.SCREEN_WIDTH - fon_money.get_width() - size_line + 5,
                                  size_line + fon_money.get_height() // 2 - money_icon.get_height() // 2))

        surface.blit(money_text,
                     (CONST.SCREEN_WIDTH - fon_money.get_width() // 2 - size_line - len(str(CONST.money)) * 5,
                      fon_money.get_height() // 2 - font_min.get_height() // 2 + size_line // 1.5))

        button_group_shop.update(surface)

        pygame.display.flip()


def overwrite_money_in_text_files():
    lines = open('data/txt_files/saves.txt', 'r', encoding='utf-8').readlines()[1:]
    with open('data/txt_files/saves.txt', 'w', encoding='utf-8') as file:
        file.seek(0, 0)
        file.write(f'money = {CONST.money}\n' + ''.join(lines))


def overwrite_difficulty_in_text_files(index_difficulty):
    lines = open('data/txt_files/saves.txt', 'r', encoding='utf-8').readlines()
    with open('data/txt_files/saves.txt', 'w', encoding='utf-8') as file:
        file.write(lines[0])
        file.write(f'difficulty_ratio = {index_difficulty}\n' + ''.join(lines[2:]))


def overwrite_character_in_text_files(index_characters):
    lines = open('data/txt_files/saves.txt', 'r', encoding='utf-8').readlines()
    with open('data/txt_files/saves.txt', 'w', encoding='utf-8') as file:
        file.write(''.join(lines[:2]))
        file.write(f'index_characters = {index_characters}\n' + ''.join(lines[3:]))


def is_it_possible_to_use_a_character(character_index):
    character = str(
        open('data/txt_files/saves.txt', 'r', encoding='utf-8').readlines()[3 + character_index].split()[-1])
    # if purchased
    if character == "+":
        return True
    # if you bought it
    elif CONST.character_price[character_index] <= CONST.money:
        # we write in the file that the character has been acquired
        lines = open('data/txt_files/saves.txt', 'r', encoding='utf-8').readlines()
        with open('data/txt_files/saves.txt', 'w', encoding='utf-8') as file:
            file.write(''.join(lines[:3 + character_index]))
            if character_index == 0:
                file.write(f'knight = +\n' + ''.join(lines[4 + character_index:]))
            elif character_index == 1:
                file.write(f'samurai = +\n' + ''.join(lines[-1]))
            else:
                file.write(f'alexandr = +')

        purchase_sound.play()
        CONST.money -= CONST.character_price[character_index]
        return True
    purchase_cancelled_sound.play()
    return False


def set_color(img, color):
    for x in range(img.get_width()):
        for y in range(img.get_height()):
            color.a = img.get_at((x, y)).a  # Preserve the alpha value.
            img.set_at((x, y), color)


button_group_menu = pygame.sprite.Group()
button_group_shop = pygame.sprite.Group()

size_button = CONST.SIZE_BUTTON
image_buttons = visual.load_image('button/button.png', transforms=size_button)
image_difficulty = visual.load_image('button/button.png', transforms=(size_button[0] - 40, size_button[1]))
difficulty_image_for_button = visual.load_image('button/button.png', transforms=(280, 130))

music_click = pygame.mixer.Sound('data/music/data_music_click_m.wav')
music_fon_menu = pygame.mixer.Sound('data/music/Oklou_Casey_MQ_-_Lurk.mp3')
music_hooked = pygame.mixer.Sound('data/music/data_music_hooked_m.wav')

# create fon
fon = pygame.transform.scale(visual.load_image('fons/fon_menu.png'), (CONST.SCREEN_WIDTH, CONST.SCREEN_HEIGHT))
fon_shop = pygame.transform.scale(visual.load_image('fons/fon_shop.png'), (CONST.SCREEN_WIDTH, CONST.SCREEN_HEIGHT))
fon_money = visual.load_image('button/fon_money.png', transforms=(175, (size_font - 6) * 1.5))
money_icon = visual.load_image('playersPanel/money_icon.png', transforms=(32, 32))
fon_money.set_alpha(200)

dict_characters = {0: 'playersPanel/knight.png', 1: 'playersPanel/samurai.png', 2: 'playersPanel/alexander.png'}
dict_difficulty = {1.0: ('easy', (0, 64, 0)), 2.5: ('normal', (64, 64, 0)), 5.0: ('hard', (64, 0, 0))}

# create button
start = Button((CONST.SCREEN_WIDTH // 2 - CONST.SIZE_BUTTON[0] // 1.75, CONST.SCREEN_HEIGHT // 1.85),
               'Play', image_buttons, (size_button[0] // 2.6, size_button[1] // 20))

shop_button = Button((CONST.SCREEN_WIDTH // 2 - CONST.SIZE_BUTTON[0] // 1.75, CONST.SCREEN_HEIGHT // 1.5),
                     'Shop', image_buttons, (size_button[0] // 2.6, size_button[1] // 25))

exit_in_menu = Button((CONST.SCREEN_WIDTH // 2 - CONST.SIZE_BUTTON[0] // 1.75, CONST.SCREEN_HEIGHT // 1.25),
                      'Exit', image_buttons, (size_button[0] // 2.6, size_button[1] // 20))

exit_in_pause = Button((CONST.SCREEN_WIDTH // 2 - CONST.SIZE_BUTTON[0] // 2.35, CONST.SCREEN_HEIGHT // 1.85),
                       'Exit in menu', image_buttons, (size_button[0] // 4.5, size_button[1] // 20),
                       font_normal=font_min.render, font_min_text=font_pause_min.render, color='black')

# icon-button difficulty
text_four_characters_long = font.render('len4', False, (0, 0, 0))
text_six_characters_long = font.render('le-th6', False, (0, 0, 0))

shift_difficulty_button = (difficulty_image_for_button.get_width() // 2 - text_four_characters_long.get_width() // 2,
                           difficulty_image_for_button.get_height() // 4)
rect_button_difficulty = (size_button[0] + 10 + difficulty_image_for_button.get_width() * 0 + 30 * (0 + 1),
                          CONST.SCREEN_HEIGHT // 1.5 + 60)
button_easy = Button(rect_button_difficulty, 'easy', difficulty_image_for_button, shift_difficulty_button)

rect_button_difficulty = (size_button[0] + 10 + difficulty_image_for_button.get_width() * 2 + 30 * (2 + 1),
                          CONST.SCREEN_HEIGHT // 1.5 + 60)
button_hard = Button(rect_button_difficulty, 'hard', difficulty_image_for_button, shift_difficulty_button)

shift_difficulty_button = (difficulty_image_for_button.get_width() // 2 - text_six_characters_long.get_width() // 2,
                           difficulty_image_for_button.get_height() // 4)
rect_button_difficulty = (size_button[0] + 10 + difficulty_image_for_button.get_width() * 1 + 30 * (1 + 1),
                          CONST.SCREEN_HEIGHT // 1.5 + 60)
button_normal = Button(rect_button_difficulty, 'normal', difficulty_image_for_button, shift_difficulty_button)

# icon-button character
size_image_character = (280, 280)
knight_image = visual.load_image(dict_characters[0], transforms=size_image_character)
samurai_image = visual.load_image(dict_characters[1], transforms=size_image_character)
alexandr_image = visual.load_image(dict_characters[2], transforms=size_image_character)

rect_button_character = (size_button[0] + 10 + size_image_character[0] * 0 + 30 * (0 + 1), 100)
button_knight = Button(rect_button_character, f'buy: {CONST.character_price[0]}', knight_image,
                       (0, size_image_character[1] - 50), color='#293133')

rect_button_character = (size_button[0] + 10 + size_image_character[0] * 1 + 30 * (1 + 1), 100)
button_samurai = Button(rect_button_character, f'buy: {CONST.character_price[1]}', samurai_image,
                        (0, size_image_character[1] - 50), color='#293133')

rect_button_character = (size_button[0] + 10 + size_image_character[0] * 2 + 30 * (2 + 1), 100)
button_alexandr = Button(rect_button_character, f'buy: {CONST.character_price[2]}', alexandr_image,
                         (0, size_image_character[1] - 50), color='#293133')

# exit from pause button
pos_exit_from_shop = (10, CONST.SCREEN_HEIGHT - 80)
exit_from_shop = Button(pos_exit_from_shop,
                        'Exit in menu', image_buttons,
                        (pos_exit_from_shop[0] + size_button[0] // 6, size_button[1] // 21),
                        font_normal=font_min.render, font_min_text=font_pause_min.render, color='black')

# create inscriptions
name_game_text = font_big.render('The Last Game', False, (0, 0, 0))
shop_text = font_big.render('Shop', False, (0, 0, 0))
character_user = font_min.render('user character', False, (255, 255, 255))
knight_text = font.render('knight', False, (0, 0, 0))
alexandr_text = font.render('alexandr', False, (0, 0, 0))
samurai_text = font.render('samurai', False, (0, 0, 0))
difficulty_text = font_min.render('difficulty', False, (255, 255, 255))

name_game_text.set_alpha(200)
shop_text.set_alpha(200)

button_in_menu = [start, exit_in_menu, shop_button]
button_in_shop = [exit_from_shop, button_easy, button_normal, button_hard, button_knight, button_alexandr,
                  button_samurai]

for one_button in button_in_menu:
    button_group_menu.add(one_button)
for one_button in button_in_shop:
    button_group_shop.add(one_button)

purchase_sound = pygame.mixer.Sound('data/music/buyTrue.mp3')
purchase_cancelled_sound = pygame.mixer.Sound('data/music/buyFalse.mp3')
