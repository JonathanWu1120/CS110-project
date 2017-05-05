import pygame, pygame.font, pygame.event, pygame.draw
from pygame.locals import *


def get_key():
    while 1:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == KEYDOWN:
            if event.key == K_BACKSPACE or event.key == K_RETURN:
                return event.key
            else:
                return event.unicode
        else:
            pass


def display_box(screen, message, length, x, y):
    "Print a message in a box on the screen"
    fontobject = pygame.font.Font(None, 32)
    pygame.draw.rect(screen, (0, 0, 0),
                     (x, y, length, 32), 0)
    pygame.draw.rect(screen, (255, 255, 255),
                     (x, y, length, 32), 1)
    if len(message) != 0:
        screen.blit(fontobject.render(message, 1, (255, 255, 255)), (x, y))
    pygame.display.flip()


def ask(screen, question, x, y):
    #ask(screen, question) -> answer
    pygame.font.init()
    current_string = []
    length = len(question) * 16
    display_box(screen, question + ''.join(current_string), length, x, y)
    while 1:
        inkey = get_key()
        if inkey == K_BACKSPACE:
            current_string = current_string[0:-1]
        elif inkey == K_RETURN:
            break
        else:
            current_string.append(inkey)
        display_box(screen, question + ''.join(current_string), length, x, y)
    return ''.join(current_string)
