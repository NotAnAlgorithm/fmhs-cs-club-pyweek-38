from .. import *

class Entity(Weak_Object):
    def __init__(self, sprite: str, x: int = 0, y: int = 0):
        super().__init__(x, y, create_surface=False)
        self.fill_sprites(sprite)
        self.resize(0, c(100))

        # internals
        self.velocity = [0, 0]
        self.acceleration = [0, -0.1]
        self.move_speed = 0.1
        self.movement = 0
        self.termv = 3
        self.grounded = False

    def update(self):
        super().update()
        self.physics()

    def physics(self):
        if abs(self.velocity[0]) < 0.1:
            self.velocity[0] = 0

        ax = self.acceleration[0]
        ay = self.acceleration[1]

        # Player movement...
        if self.movement > 0:
            ax += self.move_speed
            # double turn around speed
            if self.velocity[0] < 0:
                ax += self.move_speed
        elif self.movement < 0:
            ax -= self.move_speed
            if self.velocity[0] > 0:
                ax -= self.move_speed
        else:
            if self.velocity[0] > 0:
                ax -= self.move_speed
            elif self.velocity[0] < 0:
                ax += self.move_speed

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
