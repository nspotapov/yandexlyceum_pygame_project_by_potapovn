import pygame
from settings import *
import random


def get_distance(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5


class Directions:
    RIGHT = 0
    LEFT = 1
    UP = 2
    DOWN = 3
    STAY = 4
    ALL = [RIGHT, LEFT, UP, DOWN]

    def get_negative(self, direction):
        neg = {Directions.RIGHT: Directions.LEFT,
               Directions.LEFT: Directions.RIGHT,
               Directions.DOWN: Directions.UP,
               Directions.UP: Directions.DOWN, }
        return neg[direction]


VELOCITIES = {
    Directions.RIGHT: (1, 0),
    Directions.LEFT: (-1, 0),
    Directions.UP: (0, -1),
    Directions.DOWN: (0, 1),
    None: (0, 0)
}


class Entity(pygame.sprite.Sprite):
    def __init__(self, group, image=None, collide_groups=None):
        super().__init__(group)
        if image is None:
            image = pygame.surface.Surface((CELL_SIZE,
                                            CELL_SIZE))
        self.image = image
        self.collide_groups = collide_groups
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

    def set_cords_in_board(self, x, y):
        self.rect.x = x * CELL_SIZE
        self.rect.y = y * CELL_SIZE

    def get_pos(self, centre=False):
        if centre:
            return self.rect.x - self.rect.w / 2, self.rect.y - self.rect.h / 2
        return self.rect.x, self.rect.y


class TastyPoint(Entity):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        image = pygame.surface.Surface((CELL_SIZE,
                                        CELL_SIZE))
        pygame.draw.circle(image, MEALS_COLOR, (CELL_SIZE / 2,
                                                CELL_SIZE / 2),
                           CELL_SIZE / 6)
        image.set_colorkey('black')

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)


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
        self.mask = pygame.mask.from_surface(self.images[0])
        self.rect = self.images[0].get_rect()
        self.frames_per_image = 10
        self.current_frame = 0
        self.current_img_state = 0
        self.velocity = 1
        self.current_direction = Directions.RIGHT
        self.next_direction = None
        self.image = self.images[0]
        self.ghosts_objects = []
        self.current_collide = []

    def update(self, *args, **kwargs) -> None:

        if self.can_move(self.next_direction):
            self.current_direction = self.next_direction
            self.next_direction = None

        if self.can_move(self.current_direction):
            dx, dy = VELOCITIES[self.current_direction]
            self.rect = self.rect.move(dx, dy)
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

    def can_move(self, direction):
        if direction is None:
            return False
        if self.rect.x not in range(0, BOARD_COLS * CELL_SIZE):
            if direction in [
                Directions.UP,
                Directions.DOWN
            ]:
                return False
        dx, dy = VELOCITIES[direction]

        dx, dy = self.velocity * dx, self.velocity * dy
        self.rect = self.rect.move(dx, dy)

        self.current_collide = [pygame.sprite.spritecollideany(self, _group)
                                for _group in
                                self.collide_groups]

        self.rect = self.rect.move(-dx, -dy)
        if any(self.current_collide):
            return False
        return True

    def get_all_available_directions(self):
        available_directions = []
        for direction in Directions.ALL:
            if self.can_move(direction):
                available_directions.append(direction)

        return available_directions

    def set_velocity(self, velocity):
        self.velocity = velocity / FPS


class PacMan(Animated):
    def __init__(self, *args, meals_group=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_cords_in_board(9, 16)
        self.meals_group = meals_group
        self.current_score = 0
        self.is_alive = True
        self.death_images = None
        self.velocity = 1.9

    def update(self, *args, **kwargs):
        if self.is_alive:
            super().update(*args, **kwargs)
            if self.meals_group:
                collided_sprites = [x for x in self.meals_group
                                    if pygame.sprite.collide_mask(self, x)]

                for collide in collided_sprites:
                    if collide is not None:
                        self.meals_group.remove(collide)
                        collide.kill()
                        self.current_score += 1

            if any([isinstance(x, Ghost) for x in self.current_collide]):
                self.is_alive = False

    def get_current_score(self):
        return self.current_score

    def death_animate(self):
        self.current_frame += 1
        if self.current_frame > self.frames_per_image:
            self.current_frame = 0
            self.current_img_state += 1
            self.current_img_state %= 12
        self.image = self.death_images[self.current_img_state]
        return 11 - self.current_img_state

    def set_death_sprites(self, death_sprites):
        img_count = death_sprites.get_rect().w // CELL_SIZE
        self.death_images = []

        for i in range(img_count):
            rect = pygame.Rect((i * CELL_SIZE, 0,
                                CELL_SIZE, CELL_SIZE))
            image = death_sprites.subsurface(rect)
            self.death_images.append(image)

    def set_alive(self, alive):
        self.is_alive = alive


class Ghost(Animated):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.last_available_directions = self.get_all_available_directions()
        self.ghosts_objects = []
        self.pacman_object = None
        self.pacman_detection_distance = CELL_SIZE * 4

    def update(self, *args, **kwargs) -> None:
        super().update(*args, **kwargs)

        if get_distance(self.get_pos(centre=True),
                        self.pacman_object.get_pos(centre=True)) <= CELL_SIZE * 1.01:
            self.pacman_object.set_alive(False)

        current_available_directions = self.get_all_available_directions()
        if current_available_directions:
            if current_available_directions != self.last_available_directions:
                self.last_available_directions = current_available_directions

                if self.is_pacman_is_near():
                    velocities_for_directions = {
                        direction: VELOCITIES[direction]
                        for direction in current_available_directions
                    }
                    variants = {}
                    for key, dv in velocities_for_directions.items():
                        dx, dy = dv
                        x, y = self.get_pos()
                        dx = dx * self.velocity
                        dy = dy * self.velocity
                        variants[key] = get_distance((x + dx, y + dy),
                                                     self.pacman_object.get_pos())
                    direction = min(variants, key=lambda x: variants[x])
                    self.set_direction(direction)
                else:
                    self.set_direction(random.choice(current_available_directions))

    def can_move(self, direction):
        if direction is None:
            return False
        dx, dy = VELOCITIES[direction]

        dx, dy = self.velocity * dx, self.velocity * dy
        self.rect = self.rect.move(dx, dy)

        collide = [pygame.sprite.spritecollideany(self, _group)
                   for _group in
                   self.collide_groups]

        ghost_collide = [pygame.sprite.collide_mask(self, ghost)
                         for ghost in self.ghosts_objects]

        self.rect = self.rect.move(-dx, -dy)
        if any(collide) or any(ghost_collide):
            return False
        return True

    def set_ghosts_objects(self, ghost_objects):
        self.ghosts_objects = ghost_objects
        if self in self.ghosts_objects:
            self.ghosts_objects.remove(self)

    def set_pacman_object(self, pacman_object):
        self.pacman_object = pacman_object

    def get_all_available_directions(self):
        dirs = super().get_all_available_directions()
        if self.rect.x not in range(0, BOARD_COLS * CELL_SIZE):
            if Directions.UP in dirs:
                dirs.remove(Directions.UP)
            if Directions.DOWN in dirs:
                dirs.remove(Directions.DOWN)
        return dirs

    def is_pacman_is_near(self):
        my_pos = self.get_pos()
        pacman_pos = self.pacman_object.get_pos()
        if get_distance(my_pos, pacman_pos) < self.pacman_detection_distance:
            return True
        return False
