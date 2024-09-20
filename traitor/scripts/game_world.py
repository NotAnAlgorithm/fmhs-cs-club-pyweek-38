from .. import *


class World(Scene):
    def __init__(self, *, spawn_player: bool = True):
        super().__init__()

        # internals
        self.player = None
        if spawn_player:
            self.player = Player()
            self.add_child(self.player)
        else:
            self.add_child(
                Weak_Object(0, WINDOW_SIZE[1] - c(50), WINDOW_SIZE[0], c(50))
            )

        # Create world!!!
        self.init_objects()

    def update(self):
        super().update()
        self.physics()

    def init_objects(self):
        pass  # To be overridden!!

    def physics(self):
        loop_eternally(self, World._upd_phys)

    def _upd_phys(child):  # Apply physics to all constituents
        if child.parent is not None:
            child.physics()


class Outside(World):
    def __init__(self):
        super().__init__()

    def init_objects(self):
        super().init_objects()

        self.player.x = unc(WINDOW_SIZE[0]) - unc(self.player.rect.w) - 80
        self.player.y = unc(WINDOW_SIZE[1]) - unc(self.player.rect.h) - 50
        self.player.anim_dir = 1

        self.jeep = Weak_Object(collide=False)
        self.jeep.fill_sprites("traitor/assets/jeep/")
        self.jeep.resize(0, c(100))
        self.jeep.x = unc(WINDOW_SIZE[0]) - unc(self.jeep.rect.w) - 10
        self.jeep.y = unc(WINDOW_SIZE[1]) - unc(self.jeep.rect.h) - 50
        self.add_child(self.jeep)

        self.add_child(
            Weak_Object(
                0, WINDOW_SIZE[1] - c(50), WINDOW_SIZE[0], c(50), create_surface=True
            )
        )

        self.children.append(self.children.pop(0))  # Move player in front
