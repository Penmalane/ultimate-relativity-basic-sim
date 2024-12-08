import pygame

class RewindPuddle:
    def __init__(self, x, y, radius=20):
        self.x = x
        self.y = y
        self.radius = radius
        self.surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.surf, (0, 0, 255), (radius, radius), radius)
        self.rect = self.surf.get_rect(center=(x, y))

    def draw(self, screen):
        screen.blit(self.surf, self.rect)
