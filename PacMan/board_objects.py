import pygame
import random
from settings import *


class Directions:
    STAY = 4
    DOWN = 3
    UP = 2
    LEFT = 1
    RIGHT = 0


class Bonus:
    pass


class Entity:
    def __init__(self, screen, board, img, x, y, control):
        self.img = img
        self.control = control
        self.img.set_colorkey((0, 0, 0))
        self.x = x
        self.y = y
        self.screen = screen
        self.board = board
        self.velocity = 10 / FPS

        self.direction = Directions.RIGHT
        self.current_state = 0
        self.timer = 0

    def move(self):
        x, y = self.x, self.y

        directions = {
            Directions.UP: (0, -1),
            Directions.DOWN: (0, 1),
            Directions.LEFT: (-1, 0),
            Directions.RIGHT: (1, 0),
            Directions.STAY: (0, 0)
        }
        dx, dy = directions[self.direction]

        x += dx
        y += dy

        dx *= self.velocity
        dy *= self.velocity
        x += dx
        y += dy

        c = 3

        points = [
            (x + c, y + c),
            (x + CELL_SIZE - c, y + c),
            (x + CELL_SIZE - c, y + CELL_SIZE - c),
            (x + c, y + CELL_SIZE - c)
        ]
        try:
            colors = [self.screen.get_at((int(a), int(b)))[:-1] in [BACKGROUND_COLOR,
                                                                    MEALS_COLOR] for a, b in points]
        except Exception:
            colors = [False]
        # for x1, y1 in points:
        #     pygame.draw.circle(self.screen, 'white', (x1, y1), 2)
        # print(colors)
        if not all(colors):
            self.direction = Directions.STAY
        else:
            if isinstance(self, PacMan):
                col, row = self.board.get_cords(x, y)
                if self.board.get_value(row, col) == 0:
                    self.board.set_value(row, col, 5)
                    self.control.current_score += 1
                    self.control.maximum_score = max(self.control.maximum_score,
                                                     self.control.current_score)
            self.x = x
            self.y = y

    def render(self):
        if self.direction != Directions.STAY:
            self.img.set_clip(pygame.Rect(2 * CELL_SIZE * self.direction, 0,
                                          2 * CELL_SIZE, CELL_SIZE))
            current_dir = self.img.subsurface(self.img.get_clip())

            current_dir.set_clip(
                pygame.Rect(self.current_state * CELL_SIZE, 0, CELL_SIZE, CELL_SIZE))
            current_dir = current_dir.subsurface(current_dir.get_clip())

            self.timer += 1
            self.timer %= 10
            if not self.timer:
                self.current_state += 1
                self.current_state %= 2

        else:
            self.img.set_clip(pygame.Rect(CELL_SIZE, 0, CELL_SIZE, CELL_SIZE))
            current_dir = self.img.subsurface(self.img.get_clip())

        self.screen.blit(current_dir, (self.x, self.y))

    def set_direction(self, dir):
        self.direction = dir


class Ghost(Entity):
    def __init__(self, *args):
        super(Ghost, self).__init__(*args)
        self.velocity = 20 / FPS

    def update_direction(self):
        if self.direction == Directions.STAY:
            self.direction = random.choice([Directions.UP,
                                            Directions.DOWN,
                                            Directions.LEFT,
                                            Directions.RIGHT])


class PacMan(Entity):
    def __init__(self, *args):
        super(PacMan, self).__init__(*args)
