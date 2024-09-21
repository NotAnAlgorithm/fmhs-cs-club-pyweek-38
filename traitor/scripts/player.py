from .. import *


class Player(Entity):
    def __init__(self, sprite: str = "traitor/assets/entities/agent/", *args):
        super().__init__(sprite, *args)

        # internals
        self.jump_force = -10
        self.sneak = False

    def handle_input(self, event):
        super().handle_input(event)

        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                if self.grounded and not self.sneak:
                    self.velocity[1] = self.termv

        keys = pygame.key.get_pressed()
        self.sneak = (keys[pygame.K_DOWN] or keys[pygame.K_s]) and self.grounded

        if not self.sneak:
            if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and not (
                keys[pygame.K_RIGHT] or keys[pygame.K_d]
            ):
                self.movement = -1
            elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and not (
                keys[pygame.K_LEFT] or keys[pygame.K_a]
            ):
                self.movement = 1
            else:
                self.movement = 0
        else:
            self.movement = 0

    def update(self):
        super().update()
        if self.sneak:
            if self.anim_dir % 2 == 0:
                self.index = 16
            else:
                self.index = 17

    def physics(self):
        super().physics()
