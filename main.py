import pygame

sized = 2

if __name__ == '__main__':
    # инициализация Pygame:
    pygame.init()
    # размеры окна:
    size = width, height = 224 * sized, 288 * sized
    # screen — холст, на котором нужно рисовать:
    screen = pygame.display.set_mode(size)
    # формирование кадра:
    # команды рисования на холсте
    # ...
    # ...
    # смена (отрисовка) кадра:
    pygame.display.flip()
    # ожидание закрытия окна:
    while pygame.event.wait().type != pygame.QUIT:
        pass
    # завершение работы:
    pygame.quit()