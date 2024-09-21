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
        self.rain_sfx = pygame.mixer.Sound("traitor/assets/sounds/rain.wav")
        self.rain_sfx.set_volume(0.5)
        super().__init__()

    def on_display(self):
        super().on_display()

        self.rain_sfx.play(-1)

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
        for i in range(100):
            road = Weak_Object(collide=True)
            road.sprite_sheet = self.road.sprite_sheet
            road.rects.append(self.road.sprite.get_rect())
            road.y = self.road.y
            road.x = unc(road.rect.w) * i - unc(WINDOW_SIZE[0])
            self.add_child(road)

        self.children.append(self.children.pop(0))  # Move player in front

        self.crate = Weak_Object(collide=False)
        self.crate.fill_sprites("traitor/assets/crate/")
        self.crate.resize(0, c(60))
        self.crate.sprite.fill((32, 32, 32), special_flags=pygame.BLEND_RGB_SUB)
        self.crate.x = 200
        self.crate.y = unc(WINDOW_SIZE[1]) - unc(self.crate.rect.h) - self.road_height
        self.add_child(self.crate)

        self.security = Weak_Object(collide=False)
        self.security.fill_sprites("traitor/assets/camera/")
        self.security.resize(0, c(80))
        self.security.sprite.fill((32, 32, 32), special_flags=pygame.BLEND_RGB_SUB)
        self.security.x = 0
        self.security.y = center(unc(WINDOW_SIZE[1]), unc(self.security.rect.h))
        self.add_child(self.security)

        rain = Sprite()
        rain.fill_sprites("traitor/assets/rain/")
        for i in range(len(rain.sprite_sheet)):
            rain.resize(i, WINDOW_SIZE[1] / 4)
            rain.sprite_sheet[i].fill(
                (255, 255, 255, 128), special_flags=pygame.BLEND_RGBA_MULT
            )

        def rain_upd():
            rain.frame += 1
            if rain.frame == 3:
                rain.index += 1
                rain.frame = 0
            if rain.index == len(rain.sprite_sheet):
                rain.index = 0

        def rain_render():
            rain.rect.x = -self.camera_x
            for i in range(7):
                rain.rect.y = 0
                for i in range(4):
                    Sprite.render(rain)
                    rain.rect.y += rain.rect.h
                rain.rect.x += rain.rect.w

        rain.frame = 0
        rain.update = rain_upd
        rain.render = rain_render
        self.add_child(rain)
