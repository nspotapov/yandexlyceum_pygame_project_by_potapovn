import pygame
from settings import *


class Directions:
    RIGHT = 0
    LEFT = 1
    UP = 2
    DOWN = 3


VELOCITIES = {
    Directions.RIGHT: (1, 0),
    Directions.LEFT: (-1, 0),
    Directions.UP: (0, -1),
    Directions.DOWN: (0, 1)
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
        self.frames_per_image = 10
        self.current_frame = 0
        self.current_img_state = 0
        self.velocity = 20
        self.current_direction = Directions.RIGHT
        self.next_direction = self.current_direction
        self.image = self.images[0]

    def update(self, *args, **kwargs) -> None:
        #todo
        print(self.image.get_rect(), self.current_direction,
              self.next_direction)

        if self.can_move():
            self.current_frame += 1
            if self.current_frame > self.frames_per_image:
                self.current_frame = 0
                self.current_img_state += 1
                self.current_img_state %= 2

            index = self.current_direction * 2 + self.current_img_state
            self.image = self.images[index]

            dx, dy = VELOCITIES[self.next_direction]
            dx, dy = self.velocity * dx, self.velocity * dy
            self.rect.move(dx, dy)

    def set_direction(self, direction):
        self.next_direction = direction

    def set_cords_in_board(self, x, y):
        self.rect.x = x * CELL_SIZE
        self.rect.y = y * CELL_SIZE

    def can_move(self):
        direction = self.next_direction
        last_rect = self.rect.copy()
        dx, dy = VELOCITIES[direction]
        _x, _y = last_rect.x, last_rect.y
        _x += dx * self.velocity
        _y += dy * self.velocity
        if any([pygame.sprite.spritecollideany(self, _group) for _group in self.collide_groups]):
            return True
        return True


class PacMan(Animated):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_cords_in_board(0, 10)


class Ghost(Animated):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
