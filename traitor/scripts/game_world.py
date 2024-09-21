from .. import *


class World(Scene):
    def __init__(self, *, spawn_player: bool = True):
        super().__init__()

        # internals
        self.player = None
        if spawn_player:
            self.player = Player()
            self.add_child(self.player)
            self.world_edge_right = unc(WINDOW_SIZE[0]) - unc(self.player.rect.w)
            # unc(WINDOW_SIZE[0]) == 800.0 always
        else:
            self.add_child(
                Weak_Object(0, WINDOW_SIZE[1] - c(50), WINDOW_SIZE[0], c(50))
            )

        # Create world!!!
        self.init_objects()

    def update(self):
        super().update()
        self.physics()
        if self.player is not None:
            if self.camera_frame == self.camera_delay:
                self.camera_x = int(
                    (self.camera_x + WINDOW_SIZE[0] // 2 - self.player.rect.x) / 2
                )
                self.camera_frame = 0
            self.camera_frame += 1

    def init_objects(self):
        pass  # To be overridden!!

    def physics(self):
        loop_eternally(self, World._upd_phys)

    def _upd_phys(child):  # Apply physics to all constituents
        if child.parent is not None:
            child.physics()


class Outside(World):
    def __init__(self):
        self.road_height = 20
        super().__init__()

    def on_display(self):
        super().on_display()

    def update(self):
        super().update()
        self.background.rect.x = -self.camera_x

    def init_objects(self):
        super().init_objects()

        self.background = Weak_Object(collide=False)
        self.background.fill_sprites("traitor/assets/night_sky")
        self.background.resize(0, WINDOW_SIZE[1] * 1.2)
        self.background.sprite.fill((64, 64, 64), special_flags=pygame.BLEND_RGB_SUB)
        self.add_child(self.background)

        self.player.x = self.world_edge_right - 80
        self.player.y = unc(WINDOW_SIZE[1]) - unc(self.player.rect.h) - self.road_height
        self.player.anim_dir = 1

        self.jeep = Weak_Object(collide=False)
        self.jeep.fill_sprites("traitor/assets/jeep/")
        self.jeep.resize(0, c(100))
        self.jeep.sprite.fill((32, 32, 32), special_flags=pygame.BLEND_RGB_SUB)
        self.jeep.x = unc(WINDOW_SIZE[0]) - unc(self.jeep.rect.w) - 10
        self.jeep.y = unc(WINDOW_SIZE[1]) - unc(self.jeep.rect.h) - self.road_height
        self.add_child(self.jeep)

        self.road = Weak_Object()
        self.road.fill_sprites("traitor/assets/road/")
        self.road.resize(0, c(self.road_height))
        self.road.sprite.fill((64, 64, 64), special_flags=pygame.BLEND_RGB_SUB)
        self.road.y = unc(WINDOW_SIZE[1]) - self.road_height
        for i in range(10):
            road = Weak_Object(collide=True)
            road.sprite_sheet = self.road.sprite_sheet
            road.rects.append(self.road.sprite.get_rect())
            road.y = self.road.y
            road.x = unc(road.rect.w) * i - unc(WINDOW_SIZE[0])
            self.add_child(road)

        self.children.append(self.children.pop(0))  # Move player in front
