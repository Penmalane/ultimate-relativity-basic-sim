import pygame
import math
from rotating_arrows import RotatingArrow

class Pylon(pygame.sprite.Sprite):
    def __init__(self, x, y, status, radius=30):
        super(Pylon, self).__init__()
        self.surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        self.rect = self.surf.get_rect(center=(x, y))
        self.radius = radius
        self.status = status
        self.arrows = None
        self.createArrows()

        # Draw the pylon (yellow circle) on its surface
        pygame.draw.circle(self.surf, self.getColor(), (radius, radius), radius)

    def draw(self, screen):
        # Draw the pylon
        screen.blit(self.surf, self.rect)

        # Update arrow's visibility and draw if visible
        self.arrows.update()  # Update arrow's visibility
        if self.arrows.visible:            
            self.arrows.draw(screen)  # Draw the arrow only if it is visible

    def getColor(self):
        if self.status == 'fast':
            return (255, 255, 0)
        elif self.status == 'slow':
            return (255, 0, 255)
        else:
            return (255, 255, 255)

    def createArrows(self):
        # Determine the rotation delay based on pylon status
        if self.status == 'fast':
            rotation_delay = 12  # 12 seconds for "fast"
        elif self.status == 'slow':
            rotation_delay = 22  # 22 seconds for "slow"
        else:
            rotation_delay = 32  # 32 seconds for "none"
        
        # Create a rotating arrow for each pylon
        self.arrows = RotatingArrow(self, rotation_delay)
