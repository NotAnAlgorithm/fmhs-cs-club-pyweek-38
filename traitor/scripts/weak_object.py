from .. import *


# Weak objects are immutable, physics-less objects.
# They *can* be collided with.
class Weak_Object(Sprite):
    def __init__(
        self,
        x: int = 0,
        y: int = 0,
        w: int = 0,
        h: int = 0,
        *,
        create_surface: bool = False,
        collide: bool = True
    ):
        super().__init__()

        # internals
        self._x, self._y = x, y
        if create_surface:
            self.rects.append(pygame.Rect(x, y, w, h))
            self.sprite_sheet.append(pygame.Surface((w, h)))
            self.sprite.fill((128, 128, 0))
        self.collide = collide

    def update(self):
        super().update()

    def physics(self):
        pass  # to be overridden

    def check_collide(self):
        for each in self.parent.children:
            if isinstance(each, Weak_Object):
                if each.guid == self.guid or not each.collide:
                    continue
                if self.rect.colliderect(each.rect):
                    yield each

    @property
    def x(self):
        """
        When working with WINDOW_SIZE in object locations, you MUST unc(WINDOW_SIZE[i])
        """
        return self._x

    @x.setter
    def x(self, x):
        self._x = x
        self.rect.x = c(x)

    @property
    def y(self):
        """
        When working with WINDOW_SIZE in object locations, you MUST unc(WINDOW_SIZE[i])
        """
        return self._y

    @y.setter
    def y(self, y):
        self._y = y
        self.rect.y = c(y)
