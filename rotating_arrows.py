import pygame
import random

class RotatingArrow(pygame.sprite.Sprite):
    def __init__(self, pylon, rotation_delay):
        super().__init__()
        self.pylon = pylon
        self.direction = random.choice(["clockwise", "counterclockwise"])
        
        if self.direction == "clockwise":
            self.image = pygame.image.load("assets/arrows/cw.png").convert_alpha()  # Load the arrow image
        else:            
            self.image = pygame.image.load("assets/arrows/ccw.png").convert_alpha()  # Load the arrow image

        # Scale the arrow to be 150% of the pylon radius
        new_width = int(self.pylon.radius * 2 * 2)  # 150% of pylon's diameter
        new_height = int(self.pylon.radius * 2 * 2)
        self.image = pygame.transform.scale(self.image, (new_width, new_height))
        
        self.rect = self.image.get_rect(center=self.pylon.rect.center)
        self.rotation_delay = rotation_delay  # Time to wait before starting the visibility
        self.start_time = pygame.time.get_ticks()  # Start time to handle the delay
        self.visible = False  # Initially, the arrow is not visible
        self.visibility_duration = 5000  # Arrow stays visible for 5 seconds (5000 ms)
        self.visible_start_time = None  # Time when the arrow becomes visible
        self.ended = False

    def update(self):
        if not self.ended: 
            current_time = pygame.time.get_ticks()

            # Only make the arrow visible after the timer expires
            if current_time - self.start_time >= self.rotation_delay * 1000 and not self.visible:
                self.visible = True  # Arrow becomes visible after the timer expires
                self.visible_start_time = current_time  # Record when the arrow becomes visible

            # Hide the arrow after 4 seconds
            if self.visible and current_time - self.visible_start_time >= self.visibility_duration:
                self.visible = False  # Arrow disappears after the visibility duration
                self.ended = True

    def draw(self, screen):
        if self.visible:
            screen.blit(self.image, self.rect)
