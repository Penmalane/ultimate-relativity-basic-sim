import pygame

class CircleEffect(pygame.sprite.Sprite):
    def __init__(self, x, y, color, size):
        super().__init__()
        self.x = x
        self.y = y
        self.color = color
        self.size = size
        self.surf = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.surf, (*self.color, 128), (size, size), size)
        self.rect = self.surf.get_rect(center=(x, y))
        self.start_time = pygame.time.get_ticks()  # When the effect was created
        self.duration = 3000  # 3 seconds duration

    def update(self):
        # If more than 1 second has passed, the circle should disappear
        if pygame.time.get_ticks() - self.start_time >= self.duration:
            return False  # Effect has ended
        return True  # Effect is still active

    def draw(self, screen):
        screen.blit(self.surf, self.rect)
