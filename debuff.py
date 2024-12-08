# debuff.py (modification)
from config import DEBUFF_IMAGES, REWIND_TIMER, DEBUFF_IMAGES
from circle_effect import CircleEffect
import pygame

class Debuff:
    def __init__(self, debuff_type, duration, player=None, arena=None):
        self.image = pygame.image.load(DEBUFF_IMAGES[debuff_type])
        self.rect = self.image.get_rect()
        self.duration = duration * 1000  # Convert seconds to milliseconds
        self.start_time = pygame.time.get_ticks()
        self.debuff_type = debuff_type
        self.player = player
        self.arena = arena  # Arena is passed in to access the rewind_puddle

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time >= self.duration:
            if self.debuff_type == "rewind":
                if self.player and self.arena:
                    self.arena.set_rewind_puddle(self.player.rect.center)
                # Return the new debuff ("rewinding") and its duration
                return "rewinding", REWIND_TIMER - self.duration // 1000  # Duration of "rewinding" (40 - original duration)
            if self.debuff_type == "rewinding":
                if self.player and self.arena:
                    # When "rewinding" expires, teleport the player and stun them
                    if self.arena.rewind_puddle:  # Check if rewind_puddle exists
                        self.player.teleport(self.arena.rewind_puddle.rect.center)
                        self.player.stun()  # Stun the player for 5 seconds
                        return "stunned", 5
                    else:
                        print("Error: RewindPuddle is None!")
                return False  # Expired "rewinding" debuff

            # Create the CircleEffect when the debuff expires
            if self.debuff_type == "fire":
                color = (255, 0, 0)  # Red
                size = 150  # Medium size
            elif self.debuff_type == "spread":
                color = (128, 0, 128)  # Purple
                size = 150  # Medium size

            elif self.debuff_type == "ice":
                color = (0, 255, 255)  # Teal
                size = 150  # Big size
            elif self.debuff_type == "stack":
                color = (255, 255, 0)  # Yellow
                size = 150  # Medium size
            elif self.debuff_type == "eye":
                color = (128, 0, 128)  # Dark purple
                size = 70  # Small size
            else:
                color = (255, 255, 255)  # Default color (White)
                size = 0  # Default size

            # Create a circle effect and return it
            if self.player:
                return CircleEffect(self.player.rect.centerx, self.player.rect.centery, color, size)

            return False  # Expired debuff (no visual effect)

        return True  # The debuff is still active

    def remaining_time(self):
        current_time = pygame.time.get_ticks()
        remaining_time = max(0, (self.duration - (current_time - self.start_time)) // 1000)
        return remaining_time

    def draw(self, screen, position, font):
        self.rect.topleft = position
        screen.blit(self.image, self.rect)

        remaining_time_text = font.render(str(self.remaining_time()), True, (255, 255, 255))
        text_rect = remaining_time_text.get_rect(center=(self.rect.centerx, self.rect.bottom + 15))
        screen.blit(remaining_time_text, text_rect)
