import pygame
from player import Player
from arena import Arena
from debuff import Debuff
from config import SCREEN_WIDTH, SCREEN_HEIGHT, UNFREEZE_EVENT, dps_debuff_configuration, support_debuff_configuration
from circle_effect import CircleEffect

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# Initialize pygame
pygame.init()

# Create the screen object
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Button class for handling buttons in the main menu
class Button:
    def __init__(self, x, y, width, height, text, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.font = pygame.font.Font(None, 36)

    def draw(self, screen):
        pygame.draw.rect(screen, (100, 100, 255), self.rect)  # Draw button with color
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)  # Draw text on the button

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

# Initialize buttons for the main menu
dps_button = Button(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2, 200, 50, "DPS")
support_button = Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 200, 50, "Support")
role = None

# Variable to control the main loop
running = True
selected_configuration = []

# Main menu function
def show_menu():
    global selected_configuration, role
    menu_running = True
    while menu_running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if dps_button.is_clicked(mouse_pos):
                    role = "dps"
                    menu_running = False
                elif support_button.is_clicked(mouse_pos):
                    role = "support"
                    menu_running = False

        screen.fill((0, 0, 0))  # Clear the screen
        dps_button.draw(screen)
        support_button.draw(screen)
        pygame.display.flip()

def get_configuration():
    global role, selected_configuration
    if role == 'dps':        
        selected_configuration = dps_debuff_configuration()  # Define your Support configuration
    else:      
        selected_configuration = support_debuff_configuration()  # Define your Support configuration

def reset():
    global arena, role, debuffs, selected_configuration, circle_effects, reset_timer, current_time, player
    player.reset()
    debuffs = []  # Clear debuffs
    arena = Arena(500, "assets/arena.png")
    get_configuration()
    for debuff_type, duration in selected_configuration:
        debuffs.append(Debuff(debuff_type, duration, player, arena))
    circle_effects = []  # Clear any ongoing circle effects
    reset_timer = current_time  # Reset the timer

# Show the menu and get the user's choice
show_menu()

get_configuration()

# Create the Arena object
arena = Arena(500, "assets/arena.png")  # Adjust the radius as needed

# Instantiate player
player = Player(arena, role)

# List to store active debuffs
debuffs = []

# Add the debuffs from the selected configuration
for debuff_type, duration in selected_configuration:
    debuffs.append(Debuff(debuff_type, duration, player, arena))  # Pass player and arena to the debuffs

# List to store circle effects
circle_effects = []

# Main game loop
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# Time tracker for resetting the game (in milliseconds)
reset_timer = 0
reset_interval = 50000  # Reset every 50 seconds (50000 milliseconds)

# Main loop
while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            if event.key == pygame.K_r:
                reset()
        elif event.type == QUIT:
            running = False
        elif event.type == UNFREEZE_EVENT:  # This event is triggered when the stun duration ends
            player.unfreeze()  # Unfreeze the player after 5 seconds

    # Get all the keys currently pressed
    pressed_keys = pygame.key.get_pressed()

    # Update the player sprite based on user keypresses
    player.update(pressed_keys)

    # Update debuffs
    active_debuffs = []
    for debuff in debuffs:
        result = debuff.update()
        if result is True:
            # Keep active debuff
            active_debuffs.append(debuff)
        elif isinstance(result, CircleEffect):
            # If the debuff expired and created a circle effect, add it to the list
            circle_effects.append(result)
        elif isinstance(result, tuple):
            # If the debuff expired and is a "rewind", add the "rewinding" debuff
            debuff_type, duration = result
            debuffs.append(Debuff(debuff_type, duration, player, arena))  # Add "rewinding" debuff
        elif debuff.debuff_type == "rewind" and debuff.has_expired():
            # If "rewind" expired, add "stunned" debuff
            debuffs.append(Debuff("stunned", 5000, player, arena))  # "stunned" lasts for 5 seconds

    debuffs = active_debuffs  # Update the debuff list with active debuffs

    # Draw everything
    screen.fill((0, 0, 0))  # Clear the screen
    arena.draw(screen)      # Draw the arena
    screen.blit(player.surf, player.rect)  # Draw the player

    # Draw active debuffs horizontally at the top-right
    debuff_position_x = SCREEN_WIDTH - 100  # Start position (from the right)
    debuff_position_y = 20  # Top margin
    spacing = 100  # Horizontal spacing between debuffs
    for i, debuff in enumerate(debuffs):
        position = (debuff_position_x - i * spacing, debuff_position_y)
        debuff.draw(screen, position, font)

        # If the debuff is "rewind", draw the RewindPuddle
        if debuff.debuff_type == "rewind" and arena.rewind_puddle:
            arena.rewind_puddle.draw(screen)

    # Update and draw circle effects
    for effect in circle_effects[:]:
        if not effect.update():  # Remove the effect after it expires
            circle_effects.remove(effect)
        else:
            effect.draw(screen)

    # Update the display
    pygame.display.flip()

    # Check if 50 seconds have passed (50000 milliseconds)
    current_time = pygame.time.get_ticks()
    if current_time - reset_timer >= reset_interval:
        reset()

    clock.tick(60)  # Maintain 60 FPS
