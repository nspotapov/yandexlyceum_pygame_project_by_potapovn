import pygame
from settings import *
import random

class Directions:
    RIGHT = 0
    LEFT = 1
    UP = 2
    DOWN = 3
    STAY = 4
    ALL = [RIGHT, LEFT, UP, DOWN]


VELOCITIES = {
    Directions.RIGHT: (1, 0),
    Directions.LEFT: (-1, 0),
    Directions.UP: (0, -1),
    Directions.DOWN: (0, 1),
    None: (0, 0)
}


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
        self.collide_groups = collide_groups
        if collide_groups is None:
            self.collide_groups = []
        for i in range(self.img_count):
            rect = pygame.Rect((i * CELL_SIZE, 0,
                                CELL_SIZE, CELL_SIZE))
            image = self.image.subsurface(rect)
            self.images.append(image)
        self.rect = self.images[0].get_rect()
        self.frames_per_image = 10
        self.current_frame = 0
        self.current_img_state = 0
        self.velocity = 100 / FPS
        self.current_direction = Directions.RIGHT
        self.next_direction = None
        self.image = self.images[0]

    def update(self, *args, **kwargs) -> None:
        if self.can_move(self.next_direction):
            self.current_direction = self.next_direction
            self.next_direction = None

        if self.can_move(self.current_direction):
            self.current_frame += 1
            if self.current_frame > self.frames_per_image:
                self.current_frame = 0
                self.current_img_state += 1
                self.current_img_state %= 2

            index = self.current_direction * 2 + self.current_img_state
            self.image = self.images[index]

            if self.rect.x < -self.rect.w:
                self.rect.x = BOARD_COLS * CELL_SIZE
            elif self.rect.x > BOARD_COLS * CELL_SIZE:
                self.rect.x = -self.rect.w
        else:
            index = self.current_direction * 2 + 1
            self.image = self.images[index]

    def set_direction(self, direction):
        self.next_direction = direction
        if self.can_move(self.next_direction):
            self.current_direction = self.next_direction
            self.next_direction = None

    def set_cords_in_board(self, x, y):
        self.rect.x = x * CELL_SIZE
        self.rect.y = y * CELL_SIZE

    def can_move(self, direction):
        if direction is None:
            return False
        dx, dy = VELOCITIES[direction]

        dx, dy = self.velocity * dx, self.velocity * dy
        self.rect = self.rect.move(dx, dy)
        collide = [bool(pygame.sprite.spritecollideany(self, _group)) for _group in
                   self.collide_groups]

        if any(collide):
            self.rect = self.rect.move(-dx, -dy)
            return False
        return True

    def set_velocity(self, velocity):
        self.velocity = velocity / FPS


class PacMan(Animated):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_cords_in_board(9, 16)


class Ghost(Animated):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def update(self, *args, **kwargs) -> None:
        super().update(*args, **kwargs)
        if not self.can_move(self.current_direction):
            self.set_direction(random.choice(Directions.ALL))
