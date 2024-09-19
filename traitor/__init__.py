import pygame, sys, os, copy, json, threading, queue
from dataclasses import dataclass, field
from uuid import uuid4

from pygame.locals import *

fps_timer = pygame.time.Clock()
pygame.init()

scale = 50  # 120 is 1920x1080
WINDOW_SIZE = (16 * scale, 9 * scale)
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Traitor")

q = queue.Queue()
update_event = threading.Event()

# Game modules
from .util import *
from .models import *
from .scripts.textbox import Textbox
from .scripts.player import Player, Entity
from .scripts.title import title_screen
from .scripts.game_world import World
from .scripts.game_logic import game_logic
from .__main__ import main
