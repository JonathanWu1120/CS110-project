import pygame


class Button:
    def __init__(self, image, dimensions=(0, 0), location=(0, 0)):
        self.image = pygame.transform.scale(pygame.image.load(image), dimensions).convert_alpha()
        self.dimensions = dimensions
        self.location = location
        self.rect = pygame.rect.Rect(location, dimensions)
