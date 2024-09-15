import pygame, sys
from dataclasses import dataclass, field
from uuid import uuid4

from pygame.locals import *

fps_timer = pygame.time.Clock()
pygame.init()

WINDOW_SIZE = (600, 400)
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption('Traitor')

# Game modules
from .models import *
from .__main__ import main
