import pygame

from settings import *
from .board import Board


class GameControl:
    def __init__(self):
        self.IN_GAME = True
        self.current_window = None
        self.game_objects = []

        self.current_score = 0
        self.maximum_score = 0

        self.WIDTH = BOARD_COLS * CELL_SIZE
        self.HEIGHT = BOARD_ROWS * CELL_SIZE \
                      + 2 * FONT_SIZE + CELL_SIZE \
                      + 2 * SPACE_BETWEEN

        pygame.font.init()
        self.font = pygame \
            .font.Font(FONT_FILE, FONT_SIZE)

        pygame.init()
        self.screen = pygame.display \
            .set_mode((self.WIDTH,
                       self.HEIGHT))

        pygame.display.set_caption('PacMan')

        self.clock = pygame.time.Clock()

        self.game_objects.append(
            Board(y=2 * FONT_SIZE + 3 * SPACE_BETWEEN))

    def run(self):
        """Главный цикл игры"""
        while self.IN_GAME:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.IN_GAME = False

            self.screen.fill(BACKGROUND_COLOR)
            self.score_text_render()
            self.render()

            pygame.display.flip()
            self.clock.tick(FPS)
        pygame.quit()

    def render(self):
        for game_object in self.game_objects:
            game_object.render(self.screen)

    def score_text_render(self):
        text = self.font.render('HIGH SCORE', True, FONT_COLOR)
        self.screen.blit(text, (self.WIDTH - text.get_width(),
                                SPACE_BETWEEN))

        max_score = self.font.render(str(self.maximum_score),
                                     True, FONT_COLOR)
        self.screen.blit(max_score, (self.WIDTH - max_score.get_width(),
                                     2 * SPACE_BETWEEN + FONT_SIZE))
