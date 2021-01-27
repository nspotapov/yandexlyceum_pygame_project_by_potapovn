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


class PacManSprite(pygame.sprite.Sprite):
    pass


class Bomb(pygame.sprite.Sprite):
    # image = load_image("bomb.png")

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Bomb.image
        self.rect = self.image.get_rect()

    def update(self):
        pass
