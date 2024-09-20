from .. import *


class Player(Entity):
    def __init__(self, sprite: str = "traitor/assets/entities/agent/", *args):
        super().__init__(sprite, *args)

        # internals
        self.jump_force = -10

    def handle_input(self, event):
        super().handle_input(event)

        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                if self.grounded:
                    self.velocity[1] = self.termv

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
            self.movement = -1
        elif keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
            self.movement = 1
        else:
            self.movement = 0

    def update(self):
        super().update()
