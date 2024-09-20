from .. import *


class Entity(Weak_Object):
    def __init__(self, sprite: str, x: int = 0, y: int = 0):
        super().__init__(x, y, create_surface=False)
        self.fill_sprites(sprite)
        self.resize_all(c(100))

        # internals
        self.velocity = [0, 0]
        self.acceleration = [0, -0.1]
        self.move_speed = 0.1
        self.movement = 0
        self.termv = 3
        self.grounded = False

        # animation internals
        self.past_move = self.movement  # mirror, frame behind
        self.anim_dir = 0  # based on self.movement
        # 0 - still right
        # 1 - still left
        # 2 - walk right
        # 3 - walk left
        self.frame = 0

    def update(self):
        super().update()
        self.physics()

        # animation
        # pick directions
        if self.movement != self.past_move:
            self.frame = 0
            if self.movement == 0:
                if self.past_move > 0:
                    self.anim_dir = 0
                else:
                    self.anim_dir = 1
            elif self.movement > 0:
                self.anim_dir = 2
            else:
                self.anim_dir = 3
            self.past_move = self.movement
        else:
            self.frame += 1

        frame_coeff = 8 if self.grounded or self.movement == 0 else 6

        self.index = (self.frame // frame_coeff) % 4 + (4 * self.anim_dir)

    def physics(self):
        if abs(self.velocity[0]) < 0.1:
            self.velocity[0] = 0

        ax = self.acceleration[0]
        ay = self.acceleration[1]

        # Player movement...
        if self.movement > 0:
            ax += self.move_speed
            # triple turn around speed
            if self.velocity[0] < 0:
                ax += self.move_speed * 3
        elif self.movement < 0:
            ax -= self.move_speed
            if self.velocity[0] > 0:
                ax -= self.move_speed * 3
        else:
            if self.velocity[0] > 0:
                ax -= self.move_speed * 2
            elif self.velocity[0] < 0:
                ax += self.move_speed * 2

        self.velocity[0] += ax
        self.velocity[1] += ay

        if self.velocity[0] > self.termv:
            self.velocity[0] = self.termv
        if self.velocity[0] < -self.termv:
            self.velocity[0] = -self.termv

        self.x += self.velocity[0]
        for each in self.check_collide():
            if self.velocity[0] > 0:
                self.rect.right = each.rect.left
                self.velocity[0] = 0
            if self.velocity[0] < 0:
                self.rect.left = each.rect.right
                self.velocity[0] = 0
        self.y -= self.velocity[1]
        if abs(self.velocity[1]) > 1:
            self.grounded = False
        for each in self.check_collide():
            if self.velocity[1] < 0:
                self.rect.bottom = each.rect.top
                self.grounded = True
                self.velocity[1] = 0
            if self.velocity[1] > 0:
                self.rect.top = each.rect.bottom
                self.velocity[1] = 0

        self.x = unc(self.rect.x)
        self.y = unc(self.rect.y)
