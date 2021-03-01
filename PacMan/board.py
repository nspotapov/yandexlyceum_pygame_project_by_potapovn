import pygame
from settings import *

colors = {
    4: BACKGROUND_COLOR,
    1: WALLS_COLOR,
    2: DOOR_COLOR,
    0: MEALS_COLOR
}


class Board:
    def __init__(self, game_board, screen, x, y):
        self.game_board = game_board
        self.screen = screen
        self.x = x
        self.y = y

    def get_cords(self, x, y):
        x, y = x, y
        height = len(self.game_board) * CELL_SIZE
        width = len(self.game_board[0]) * CELL_SIZE

        col, row = int(((y - self.y) * BOARD_ROWS) / height), \
                   int(((x - self.x) * BOARD_COLS) / width)

        return row, col

    def get_value(self, row, col):
        try:
            value = self.game_board[row][col]
            return value
        except Exception:
            return 5

    def set_value(self, row, col, value):
        self.game_board[row][col] = value

    def render(self):
        screen = self.screen
        game_board = self.game_board
        for i, row in enumerate(game_board):
            for j, value in enumerate(row):
                x = j * CELL_SIZE + self.x
                y = i * CELL_SIZE + self.y
                w = h = CELL_SIZE
                if value:
                    pygame.draw.rect(screen, colors.get(value, BACKGROUND_COLOR),
                                     (x, y, w, h))
                else:
                    pygame.draw.circle(screen, MEALS_COLOR, (x + CELL_SIZE / 2, y + CELL_SIZE / 2),
                                       2)
