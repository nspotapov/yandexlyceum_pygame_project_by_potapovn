from settings import GAME_BOARD
from settings import CELL_SIZE
from .tiles import PacManTile


class Board:
    """Класс клеточного поля игры"""

    def __init__(self, x=0, y=0):
        self.left_top_x = x
        self.left_top_y = y
        self.current_board_state = GAME_BOARD.copy()
        self.rows_count = len(self.current_board_state)
        self.cols_count = len(self.current_board_state[0])

        self.initialize_tiles()

    def get_tile_id(self, row, col):
        """Вохвращает id тайла на карте с координатами [row][col]"""
        return self.current_board_state[row][col]

    def set_tile_id(self, row, col, tile_id):
        """Устанавливает id тайла на карту с координатами [row][col]"""
        self.current_board_state[row][col] = tile_id

    def get_current_board_state(self):
        """Возвращает текущее состояние карты"""
        return self.current_board_state.copy()

    def render(self, screen):
        """Рисует поле на холсте screen"""
        for i in range(len(self.current_board_state)):
            for j in range(len(self.current_board_state[i])):
                self.current_board_state[i][j] \
                    .render(screen,
                            self.left_top_x + j * CELL_SIZE,
                            self.left_top_y + i * CELL_SIZE)

    def get_board_width(self):
        """Возвращает ширину поля"""
        return self.cols_count * CELL_SIZE

    def get_board_height(self):
        """Возврашает высоту поля"""
        return self.rows_count * CELL_SIZE

    def initialize_tiles(self):
        for i in range(self.rows_count):
            for j in range(self.cols_count):
                tile_id = self.current_board_state[i][j]
                self.current_board_state[i][j] = PacManTile(tile_id)
