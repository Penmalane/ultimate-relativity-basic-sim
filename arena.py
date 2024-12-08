import pygame
import math
from config import SCREEN_WIDTH, SCREEN_HEIGHT
from pylon import Pylon
from rewind_puddle import RewindPuddle

class Arena:
    def __init__(self, radius, image_path):
        self.radius = radius
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (2 * radius, 2 * radius))
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.pylons = pygame.sprite.Group()
        self.create_pylons(8, radius // 2)  # Create pylons
        self.rewind_puddle = None  # This will hold the RewindPuddle instance
    
    def create_pylons(self, count, inner_radius):
        # Create pylons as before
        center_x, center_y = self.rect.center
        angle_step = 2 * math.pi / count
        for i in range(count):
            angle = i * angle_step
            x = center_x + inner_radius * math.cos(angle)
            y = center_y + inner_radius * math.sin(angle)
            status = self.getStatus(i)
            pylon = Pylon(x, y, status)
            self.pylons.add(pylon)

    def draw(self, screen):
        # Draw arena and pylons
        screen.blit(self.image, self.rect)
        for pylon in self.pylons:
            pylon.draw(screen)
        
        # Draw the rewind puddle if it exists
        if self.rewind_puddle:
            self.rewind_puddle.draw(screen)

    def getStatus(self, index):
        # Define debuff statuses as before
        if index == 2 or index == 5 or index == 7:
            return 'fast'
        elif index == 0 or index == 4:
            return 'slow'
        else:
            return 'none'

    def set_rewind_puddle(self, position):
        # Create and set the rewind puddle at the given position
        self.rewind_puddle = RewindPuddle(position[0], position[1])
