import pygame
from settings import *


class Directions:
    RIGHT = 0
    LEFT = 1
    UP = 2
    DOWN = 3


class Entity(pygame.sprite.Sprite):
    def __init__(self, group, image=None):
        super().__init__(group)
        if image is None:
            image = pygame.surface.Surface((CELL_SIZE,
                                            CELL_SIZE))
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0


class Animated(Entity):
    def __init__(self, *args, collide_groups=None):
        super().__init__(*args)
        self.img_count = self.rect.w // CELL_SIZE
        self.images = []
        if collide_groups is None:
            self.collide_groups = []
        for i in range(self.img_count):
            rect = pygame.Rect((i * CELL_SIZE, 0,
                                CELL_SIZE, CELL_SIZE))
            image = self.image.subsurface(rect)
            self.images.append(image)
        self.frames_per_image = 10
        self.current_frame = 0
        self.current_img_state = 0
        self.velocity = 20
        self.current_direction = Directions.RIGHT
        self.next_direction = None

    def update(self, *args, **kwargs) -> None:
        self.current_frame += 1
        if self.current_frame > self.frames_per_image:
            self.current_frame = 0
            self.current_img_state += 1
            self.current_img_state %= 2

        index = self.current_direction * 2 + self.current_img_state
        self.image = self.images[index]

    def set_direction(self, direction):
        self.current_direction = direction

    def set_cords_in_board(self, x, y):
        self.rect.x = x * CELL_SIZE
        self.rect.y = y * CELL_SIZE


class PacMan(Animated):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_cords_in_board(0, 10)


class Ghost(Animated):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
