import pygame, sys, os, copy
from dataclasses import dataclass, field
from uuid import uuid4

from pygame.locals import *

fps_timer = pygame.time.Clock()
pygame.init()

scale = 50  # 120 is 1920x1080
WINDOW_SIZE = (16 * scale, 9 * scale)
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Traitor")

# Game modules
from .util import *
from .models import *
from .scripts.title import title_screen
from .__main__ import main
