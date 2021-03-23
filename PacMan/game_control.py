import pygame
from pygame.locals import *
from settings import *
from .board_objects import Directions
from .program_states import ProgramState
from .sprites import *

BLINK_EVENT = pygame.USEREVENT + 1

board_x = 0
board_y = 2 * FONT_SIZE + 3 * SPACE_BETWEEN


class GameControl:
    def __init__(self):
        self.game_state = ProgramState.START

        self.all_entities = pygame.sprite.Group()
        self.ghosts = pygame.sprite.Group()
        self.players = pygame.sprite.Group()
        self.walls_group = pygame.sprite.Group()
        self.meals_group = pygame.sprite.Group()
        self.meals_obj_group = []

        self.ghosts_objects = []

        ghost_collide_groups = [
            self.walls_group,
            self.players,
        ]

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

        self.board_screen = self.screen.subsurface((board_x, board_y,
                                                    BOARD_COLS * CELL_SIZE,
                                                    BOARD_ROWS * CELL_SIZE))

        pygame.display.set_caption('PacMan')

        self.clock = pygame.time.Clock()
        pygame.time.set_timer(BLINK_EVENT, 500)

        images = pygame.image.load('resources/assets/sprites.png')
        images.set_colorkey('black')

        rect = pygame.Rect((0, 0, 8 * CELL_SIZE, CELL_SIZE))
        image = images.subsurface(rect)
        self.player = PacMan(self.players, image,
                             collide_groups=[self.walls_group, self.ghosts],
                             meals_group=self.meals_obj_group)
        self.all_entities.add(self.player)
        self.players.add(self.player)

        rect = pygame.Rect((0, CELL_SIZE, 8 * CELL_SIZE, CELL_SIZE))
        image = images.subsurface(rect)
        self.blinky = Ghost(self.ghosts, image,
                            collide_groups=ghost_collide_groups)
        self.all_entities.add(self.blinky)
        self.ghosts.add(self.blinky)
        self.blinky.set_cords_in_board(9, 10)

        rect = pygame.Rect((0, 2 * CELL_SIZE, 8 * CELL_SIZE, CELL_SIZE))
        image = images.subsurface(rect)
        self.pinky = Ghost(self.ghosts, image,
                           collide_groups=ghost_collide_groups)
        self.all_entities.add(self.pinky)
        self.ghosts.add(self.pinky)
        self.pinky.set_cords_in_board(9, 11)

        rect = pygame.Rect((0, 3 * CELL_SIZE, 8 * CELL_SIZE, CELL_SIZE))
        image = images.subsurface(rect)
        self.inky = Ghost(self.ghosts, image,
                          collide_groups=ghost_collide_groups)
        self.all_entities.add(self.inky)
        self.ghosts.add(self.inky)
        self.inky.set_cords_in_board(9, 12)

        rect = pygame.Rect((0, 4 * CELL_SIZE, 8 * CELL_SIZE, CELL_SIZE))
        image = images.subsurface(rect)
        self.clyde = Ghost(self.ghosts, image,
                           collide_groups=ghost_collide_groups)
        self.all_entities.add(self.clyde)
        self.ghosts.add(self.clyde)
        self.clyde.set_cords_in_board(9, 8)

        self.ghosts_objects = [
            self.clyde,
            self.inky,
            self.pinky,
            self.blinky,
        ]

        for ghost in self.ghosts_objects:
            ghost.set_ghosts_objects(self.ghosts_objects.copy())

        for i in range(len(INITIAL_GAME_BOARD)):
            for j in range(len(INITIAL_GAME_BOARD[0])):
                value = INITIAL_GAME_BOARD[i][j]
                image = pygame.surface.Surface((CELL_SIZE,
                                                CELL_SIZE))
                if value == 1:
                    pygame.draw.rect(image, WALLS_COLOR,
                                     (0, 0, CELL_SIZE, CELL_SIZE))

                    temp_sprite = Entity(self.walls_group, image)
                    temp_sprite.rect.x = j * CELL_SIZE
                    temp_sprite.rect.y = i * CELL_SIZE
                elif value == 3:
                    if self.ghosts_objects:
                        ghost = self.ghosts_objects.pop()
                        ghost.set_cords_in_board(j, i)

                if value == 0:
                    meal = TastyPoint(self.meals_group,
                                      collide_groups=[self.players])
                    meal.set_cords_in_board(j, i)
                    self.meals_group.add(meal)
                    self.meals_obj_group.append(meal)

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

            elif self.game_state == ProgramState.IN_GAME:
                self.all_entities.update()
                self.current_score = self.player.get_current_score()
                self.maximum_score = max(self.current_score,
                                         self.maximum_score)
                if not self.player.is_alive:
                    self.game_state = ProgramState.GAME_OVER
            elif self.game_state == ProgramState.GAME_OVER:
                print('GAME OVER')

            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()

    def render(self):
        self.walls_group.draw(self.board_screen)
        self.meals_group.draw(self.board_screen)
        self.all_entities.draw(self.board_screen)

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
