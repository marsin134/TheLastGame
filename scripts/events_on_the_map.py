import pygame
from .visual import load_image
from scripts.constants import TILE_WIDTH, TILE_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT


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
