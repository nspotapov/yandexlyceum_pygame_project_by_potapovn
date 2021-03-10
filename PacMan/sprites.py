import pygame
from settings import *


class Directions:
    RIGHT = 0
    LEFT = 1
    UP = 2
    DOWN = 3


class Entity(pygame.sprite.Sprite):
    def __init__(self, group, image=None):
        super(Entity, self).__init__(group)
        if image is None:
            image = pygame.surface.Surface((CELL_SIZE,
                                            CELL_SIZE))
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

    def update(self, *args, **kwargs) -> None:
        pass


class Animated(Entity):
    def __init__(self, *args):
        super(Animated, self).__init__(*args)
        self.img_count = self.rect.w // CELL_SIZE
        self.images = []
        for i in range(self.img_count):
            rect = pygame.Rect((i * CELL_SIZE, 0,
                                CELL_SIZE, CELL_SIZE))
            image = self.image.subsurface(rect)
            self.images.append(image)

        self.current_img_state = 0
        self.velocity = 20
        self.direction = Directions.RIGHT

    def update(self, *args, **kwargs) -> None:
        self.current_img_state += 1
        self.current_img_state %= 2
        index = self.direction + self.current_img_state
        self.image = self.images[index]


class PacMan(Animated):
    def __init__(self, *args):
        super(Animated, self).__init__(*args)

    def update(self, *args, **kwargs) -> None:
        pass


class Ghost(Animated):
    def __init__(self, *args):
        super(Ghost, self).__init__(*args)

    def update(self, *args, **kwargs) -> None:
        pass
