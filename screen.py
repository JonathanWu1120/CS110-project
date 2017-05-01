import pygame

def make_screen():
    pygame.init()
    screen = pygame.display.set_mode((360,800))
    background = pygame.Surface((360,800))
    gray = (255,255,255)
    grey = (200,200,200)
    red = (00,0,100)
    orange = (255,140,0)
    background.fill(grey)
    screen.blit(background,(0,0))
    return screen

