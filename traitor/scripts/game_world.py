from .. import *


# How do I even go about creating a game world?
class World(Scene):
    def __init__(self, *, spawn_player: bool = True):
        super().__init__()

        # internals
        if spawn_player:
            self.add_child(Player())
        self.add_child(Weak_Object(0, WINDOW_SIZE[1] - c(50), WINDOW_SIZE[0], c(50)))

    def update(self):
        super().update()
        self.physics()

    def physics(self):
        loop_eternally(self, World._upd_phys)

    def _upd_phys(child):  # Apply physics to all constituents
        if child.parent is not None:
            child.physics()
