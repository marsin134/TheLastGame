import pygame
from scripts import visual, characters, events_on_the_map, constants, enemy, boss

SIZE = WIDTH, HEIGHT = constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT

screen = pygame.display.set_mode(SIZE)

# creating an icon and a window name
pygame_icon = pygame.image.load('data/image/facilities/statue.png')
pygame.display.set_icon(pygame_icon)
pygame.display.set_caption('The Last Game')

# inheritance of background and sprite groups
fon_game = visual.fon_game

all_sprites = visual.all_sprites
tiles_group = visual.tiles_group
clouds_group = visual.clouds_group
player_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()

# cloud creation time
cooldown = 1500
update_time = -cooldown

pause = False

# creating objects
player = characters.Alexander((WIDTH // 2 - visual.TILE_WIDTH, HEIGHT - 250), tiles_group, enemy_group, player_group)

statue = events_on_the_map.Statue(all_sprites)

wave = events_on_the_map.Wave(statue, player, tiles_group, enemy_group)

clock = pygame.time.Clock()
FPS = 30

running = True

events_on_the_map.fon_game_music_waterflame.play(-1)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pause = not pause

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
        visual.display_text(screen, 'Pause', 100, 1000)
        screen.blit(visual.image_grey, (0, 0))

    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()
