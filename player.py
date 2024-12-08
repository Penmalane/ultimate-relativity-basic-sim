import pygame
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT
)
from config import SCREEN_WIDTH, SCREEN_HEIGHT, UNFREEZE_EVENT

dx = 5
dy = 5

class Player(pygame.sprite.Sprite):
    def __init__(self, arena, role):
        super(Player, self).__init__()
        if role == 'dps':
            self.surf = pygame.image.load("assets/player/dps.png").convert()
        else:
            self.surf = pygame.image.load("assets/player/support.png").convert()
            
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(center=arena.rect.center)
        self.is_stunned = False  # To track if the player is stunned
        self.arena = arena  # The arena object

    def update(self, pressed_keys):
        if self.is_stunned:
            return  # Don't allow movement if the player is stunned

        dx = dy = 5
        if pressed_keys[K_UP]:
            if self.rect.top - dy >= self.arena.rect.top:  # Check if the player is within the arena's top boundary
                self.rect.move_ip(0, -dy)

        if pressed_keys[K_DOWN]:
            if self.rect.bottom + dy <= self.arena.rect.bottom:  # Check if the player is within the arena's bottom boundary
                self.rect.move_ip(0, dy)

        if pressed_keys[K_LEFT]:
            if self.rect.left - dx >= self.arena.rect.left:  # Check if the player is within the arena's left boundary
                self.rect.move_ip(-dx, 0)

        if pressed_keys[K_RIGHT]:
            if self.rect.right + dx <= self.arena.rect.right:  # Check if the player is within the arena's right boundary
                self.rect.move_ip(dx, 0)

    def teleport(self, position):
        self.rect.center = position  # Teleport the player to the new position

    def stun(self):
        self.is_stunned = True
        pygame.time.set_timer(UNFREEZE_EVENT, 5000)  # Stun for 5 seconds (5000 ms)

    def unfreeze(self):
        self.is_stunned = False
        pygame.time.set_timer(UNFREEZE_EVENT, 0)  # Stop the stun timer
