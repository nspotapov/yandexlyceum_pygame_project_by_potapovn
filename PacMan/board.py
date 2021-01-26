from settings import GAME_BOARD


class Board:
    def __init__(self):
        self.current_board_state = GAME_BOARD.copy()

    def get_tile_id(self, row, col):
        """Вохвращает id тайла на карте с координатами [row][col]"""
        return self.current_board_state[row][col]

    def get_current_board_state(self):
        """Возвращает текущее состояние карты"""
        return self.current_board_state.copy()

    def set_tile_id(self, row, col):
        """Устанавливает id тайла на карту с координатами [row][col]"""
        # TODO
        pass
