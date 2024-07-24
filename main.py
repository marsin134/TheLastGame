import pygame
from scripts import visual, characters, events_on_the_map, constants, menu

SIZE = WIDTH, HEIGHT = constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT

screen = pygame.display.set_mode(SIZE)

# creating an icon and a window name
pygame_icon = pygame.image.load('data/image/facilities/statue.png')
pygame.display.set_icon(pygame_icon)
pygame.display.set_caption('The Last Game')

# inheritance of background and sprite groups
fon_game = visual.fon_game

clock = pygame.time.Clock()
FPS = 30

dict_character = {0: characters.Knight,
                  1: characters.Samurai,
                  2: characters.Alexander}


def game(screen):
    # cloud creation time
    cooldown = 1500
    update_time = -cooldown

    all_sprites = visual.all_sprites
    tiles_group = visual.tiles_group
    clouds_group = visual.clouds_group
    player_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()

    pause = False

    # creating objects
    character_index = int(open('data/txt_files/saves.txt', 'r', encoding='utf-8').readlines()[2].split()[-1])
    player = dict_character[character_index]((WIDTH // 2 - visual.TILE_WIDTH, HEIGHT - 250), tiles_group, enemy_group,
                                             player_group)

    statue = events_on_the_map.Statue(all_sprites)

    wave = events_on_the_map.Wave(statue, player, tiles_group, enemy_group)

    running = True

    events_on_the_map.fon_game_music_waterflame.play(-1)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu.overwrite_money_in_text_files()
                pygame.quit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pause = not pause
            if ((pause or wave.death_player or wave.win_player)
                    and event.type == pygame.MOUSEBUTTONUP and menu.exit_in_pause.rect.collidepoint(event.pos)):
                return False

            if not pause:
                # tracking keystrokes for control
                player.events_movement(event)

        if not pause:
            screen.blit(fon_game, (0, 0))

            # creating a cloud
            if pygame.time.get_ticks() - update_time > cooldown:
                visual.Clouds(clouds_group, all_sprites)
                update_time = pygame.time.get_ticks()

            # rendering and updating sprites
            all_sprites.draw(screen)

            clouds_group.update()
            statue.update(screen)

            enemy_group.update(screen)
            player_group.update(screen)

            wave.update(screen)
        else:
            menu.exit_in_pause.update(screen)
            visual.display_text(screen, 'Pause', 100, 1000)
            screen.blit(visual.image_grey, (0, 0))

        pygame.display.flip()

        clock.tick(FPS)


run_game = menu.menu(screen)
while run_game:
    pygame.mixer.stop()
    if not game(screen):
        pygame.mixer.stop()
        run_game = menu.menu(screen)
pygame.quit()
