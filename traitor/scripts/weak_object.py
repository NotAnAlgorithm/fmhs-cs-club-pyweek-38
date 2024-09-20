from .. import *

# Weak objects are immutable, physics-less objects.
# They *can* be collided with.
class Weak_Object(Sprite):
    def __init__(self, x: int = 0, y: int = 0, w:int = 0, h:int = 0, *, create_surface:bool = True):
        super().__init__()

        # internals
        self._x, self._y = x, y
        self.rects.append(pygame.Rect(x, y, w, h))
        if create_surface:
            self.sprite_sheet.append(pygame.Surface((w, h)))
            self.sprite.fill((255, 0, 0))

    def update(self):
        super().update()
    
    def physics(self):
        pass # to be overridden
    
    def check_collide(self):
        for each in self.parent.children:
            if each.guid == self.guid:
                continue
            if isinstance(each, Weak_Object):
                if self.rect.colliderect(each.rect):
                    yield each

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
