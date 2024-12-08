
import pygame
import random

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

UNFREEZE_EVENT = pygame.event.custom_type()

# Debuff image paths (make sure these images exist)
DEBUFF_IMAGES = {
    "eye": "assets/debuffs/eye.png",
    "rewind": "assets/debuffs/rewind.png",
    "rewinding": "assets/debuffs/rewinding.png",
    "fire": "assets/debuffs/fire.png",
    "spread": "assets/debuffs/spread.png",
    "stack": "assets/debuffs/stack.png",
    "ice": "assets/debuffs/ice.png",
    "water": "assets/debuffs/water.png",
    "stunned": "assets/debuffs/stunned.png"
}

# Predefined configurations with debuff names and durations
SUPPORT_DEBUFF_CONFIGURATIONS = [
    [("eye", 42), ("rewind", 25), ("fire", 30)],
    [("spread", 42), ("rewind", 15), ("fire", 20)],
    [("spread", 42), ("rewind", 15), ("ice", 20)],
    [("spread", 42), ("rewind", 15), ("fire", 10)]
]

DPS_DEBUFF_CONFIGURATIONS = [
    [("eye", 42), ("stack", 10), ("rewind", 25), ("fire", 30)],
    [("eye", 42), ("rewind", 25), ("ice", 20)],
    [("spread", 42), ("rewind", 15), ("fire", 20)],
    [("stack", 20), ("spread", 42), ("rewind", 15), ("fire", 10)]
]

REWIND_TIMER = 40

def support_debuff_configuration():
    # Pick a random configuration
    return random.choice(SUPPORT_DEBUFF_CONFIGURATIONS)

def dps_debuff_configuration():
    # Pick a random configuration
    return random.choice(DPS_DEBUFF_CONFIGURATIONS)
