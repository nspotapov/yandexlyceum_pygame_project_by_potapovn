from settings import *
import pygame
import os


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}'"
              f" не найден")
        pygame.quit()
    image = pygame.image.load(fullname)
    if color_key is not None:
        image = image.convert()
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()

    return image


def cut_image(image: pygame.image):
    images_by_directions = {'right': [],
                            'left': [],
                            'up': [],
                            'down': []}

    for i, direction in enumerate(images_by_directions.keys()):
        images_by_directions[direction] = (
            image.get_rect((i * SPRITE_SIZE, 0,
                            (i + 1) * SPRITE_SIZE, SPRITE_SIZE)),

            image.get_rect(((i + 1) * SPRITE_SIZE, 0,
                            (i + 2) * SPRITE_SIZE, SPRITE_SIZE))
        )
    return images_by_directions


class Sprite(pygame.sprite.Sprite):
    def __init__(self, image, *group):
        super(Sprite, self).__init__(*group)
        self.image = load_image(image)
        self.images_by_directions = cut_image(self.image)
        self.images_by_directions['up'][0].show()
