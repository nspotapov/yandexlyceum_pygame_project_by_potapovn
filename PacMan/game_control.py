import pygame
from pygame.locals import *
from settings import *
from .board_objects import Entity, Directions
from .board import Board
from .program_states import ProgramState

BLINK_EVENT = pygame.USEREVENT + 1


class GameControl:
    def __init__(self):
        self.game_state = ProgramState.START
        self.current_window = None
        self.game_objects = []

        self.current_score = 0
        self.maximum_score = 0
        self.CELL_SIZE = CELL_SIZE

        self.WIDTH = BOARD_COLS * self.CELL_SIZE
        self.HEIGHT = BOARD_ROWS * self.CELL_SIZE \
                      + 2 * FONT_SIZE + self.CELL_SIZE \
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
        pygame.time.set_timer(BLINK_EVENT, 500)

        self.board = Board(INITIAL_GAME_BOARD, self.screen, 0,
                                       2 * (FONT_SIZE + SPACE_BETWEEN))

        self.game_objects.append(self.board)
        img = pygame.image.load('resources/assets/sprites.png')
        img.set_clip(pygame.Rect(0, 0, 128, 16))
        sprite = img.subsurface(img.get_clip())

        self.player = Entity(self.screen, self.board, sprite,
                             0, CELL_SIZE * 12 + 2 * SPACE_BETWEEN, self)

        self.game_objects.append(self.player)

    def run(self):
        """Главный цикл игры"""
        font_color = FONT_COLOR
        while self.game_state != ProgramState.EXIT:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_state = ProgramState.EXIT

                if event.type == BLINK_EVENT:
                    if font_color == COLOR_GREY:
                        font_color = FONT_COLOR
                    else:
                        font_color = COLOR_GREY

                if self.game_state == ProgramState.START:
                    if event.type == pygame.KEYDOWN:
                        self.game_state = ProgramState.IN_GAME

                elif self.game_state == ProgramState.IN_GAME:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.game_state = ProgramState.PAUSE
                        elif event.key == pygame.K_UP:
                            self.player.set_direction(Directions.UP)
                        elif event.key == pygame.K_DOWN:
                            self.player.set_direction(Directions.DOWN)
                        elif event.key == pygame.K_LEFT:
                            self.player.set_direction(Directions.LEFT)
                        elif event.key == pygame.K_RIGHT:
                            self.player.set_direction(Directions.RIGHT)

                elif self.game_state == ProgramState.PAUSE:
                    if event.type == pygame.KEYDOWN:
                        self.game_state = ProgramState.IN_GAME

            self.screen.fill(BACKGROUND_COLOR)
            self.score_text_render()
            self.render()

            if self.game_state == ProgramState.START:
                pygame.draw.rect(self.screen, COLOR_GREY,
                                 (0, self.HEIGHT / 2 - FONT_SIZE - 1.5 * SPACE_BETWEEN,
                                  self.WIDTH, 2 * FONT_SIZE + 3 * SPACE_BETWEEN))

                text = self.font.render('PRESS ANY KEY', True, font_color)
                self.screen.blit(text, (self.WIDTH / 2 - text.get_width() / 2,
                                        self.HEIGHT / 2 - FONT_SIZE - 0.5 * SPACE_BETWEEN))

                text = self.font.render('TO START', True, font_color)
                self.screen.blit(text, (self.WIDTH / 2 - text.get_width() / 2,
                                        self.HEIGHT / 2 + SPACE_BETWEEN))

            elif self.game_state == ProgramState.PAUSE:
                pygame.draw.rect(self.screen, COLOR_GREY,
                                 (0, self.HEIGHT / 2 - 1.5 * FONT_SIZE - 2 * SPACE_BETWEEN,
                                  self.WIDTH, 3 * FONT_SIZE + 4 * SPACE_BETWEEN))

                text = self.font.render('PAUSE', True, font_color)
                self.screen.blit(text, (self.WIDTH / 2 - text.get_width() / 2,
                                        self.HEIGHT / 2 - 1.5 * FONT_SIZE - SPACE_BETWEEN))

                text = self.font.render('PRESS ANY KEY', True, FONT_COLOR)
                self.screen.blit(text, (self.WIDTH / 2 - text.get_width() / 2,
                                        self.HEIGHT / 2 - 0.5 * FONT_SIZE))

                text = self.font.render('TO START', True, FONT_COLOR)
                self.screen.blit(text, (self.WIDTH / 2 - text.get_width() / 2,
                                        self.HEIGHT / 2 + 0.5 * FONT_SIZE + SPACE_BETWEEN))

            pygame.display.flip()
            self.clock.tick(FPS)
        pygame.quit()

    def render(self):
        for game_object in self.game_objects:
            if self.game_state == ProgramState.IN_GAME:
                if isinstance(game_object, Entity):
                    game_object.move()
            game_object.render()

    def score_text_render(self):
        text = self.font.render('SCORE', True, FONT_COLOR)
        self.screen.blit(text, (0, SPACE_BETWEEN))

        score = self.font.render(str(self.current_score), True, FONT_COLOR)
        self.screen.blit(score, (0, 2 * SPACE_BETWEEN + FONT_SIZE))

        text = self.font.render('HIGH SCORE', True, FONT_COLOR)
        self.screen.blit(text, (self.WIDTH - text.get_width(),
                                SPACE_BETWEEN))

        max_score = self.font.render(str(self.maximum_score),
                                     True, FONT_COLOR)
        self.screen.blit(max_score, (self.WIDTH - max_score.get_width(),
                                     2 * SPACE_BETWEEN + FONT_SIZE))
