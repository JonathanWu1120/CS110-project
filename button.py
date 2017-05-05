import pygame


class Button:
    def __init__(self, image, dimensions=(0, 0), location=(0, 0), text_surface=None):
        self.text_surface = text_surface
        try:
            self.image = pygame.transform.scale(pygame.image.load(image), dimensions).convert_alpha()
        except Exception:
            self.image = self.text_surface
        self.dimensions = dimensions
        self.location = location
        self.rect = pygame.rect.Rect(location, dimensions)
