from .. import *


class Entity(Sprite):
    def __init__(self, sprite: str, x: int = 0, y: int = 0):
        super().__init__()
        self.fill_sprites(sprite)
        self.resize(0, c(100))

        # internals
        self._x, self._y = x, y
        self.velocity = [0, 0]
        self.forces_x = [0] * 10
        self.forces_y = [0] * 10
        # ... did I just make a freaking free-body diagram?
        self.acceleration = [0, 0]
        self.max_velocity = c(5)
        self.move_acceleration = c(0.25)
        self.air_intensity = 1.5  # base of exponential function

        # constant forces
        self.forces_y[0] = -c(0.1)

        # map:
        # forces_x
        # [0] air resistance
        # [1] movement
        # forces_y
        # [0] gravity
        # [1] air resistance

    def update(self):
        super().update()
        self.physics()

    def physics(self):  # This is a lot of math... I should optimize
        # Subject to change... places floor at window height
        # Bounces when hitting surface while moving downwards
        if self.rect.y + self.rect.h >= WINDOW_SIZE[1]:
            self.velocity[1] = -self.velocity[1] / 2  # 2 is the bounce coefficient
            self.velocity[1] -= self.acceleration[1]

        self.x_direction = 1 if self.velocity[0] > 0 else -1
        self.y_direction = 1 if self.velocity[1] > 0 else -1
        # Calculate air resistance if moving
        if self.velocity[1] != 0:  # Vertical
            self.forces_y[1] = self.velocity[1] / abs(self.velocity[1]) * -c(0.01)
        if self.velocity[0] != 0:  # Horizontal
            self.forces_x[0] = (
                -self.x_direction
                * self.move_acceleration
                * (self.air_intensity) ** (abs(self.velocity[0]) - self.max_velocity)
            )
            if abs(self.velocity[0]) < c(
                0.05
            ):  # Too slow to matter. Just end it already.
                if self.forces_x[0] == 0:
                    self.velocity[0] = 0
                    self.forces_x[0] = 0

        self.acceleration = [0, 0]
        for force in self.forces_x:
            self.acceleration[0] += force
        for force in self.forces_y:
            self.acceleration[1] += force

        self.velocity[0] += self.acceleration[0]
        self.velocity[1] += self.acceleration[1]
        self.x += self.velocity[0]
        self.y -= self.velocity[1]

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, x):
        self._x = x
        self.rect.x = c(x)

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, y):
        self._y = y
        self.rect.y = c(y)


class Player(Entity):
    def __init__(self, sprite: str = "traitor/assets/entities/agent/", *args):
        super().__init__(sprite, *args)

    def handle_input(self, event):
        super().handle_input(event)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
            self.forces_x[1] = -self.move_acceleration
        elif keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
            self.forces_x[1] = self.move_acceleration
        else:
            self.forces_x[1] = 0

    def update(self):
        super().update()
