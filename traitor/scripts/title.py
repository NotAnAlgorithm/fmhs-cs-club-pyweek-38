from .. import *

title_screen = Scene()

city_skyline = Scene()

night_sky = Sprite()
night_sky.fill_sprites("traitor/assets/night_sky/")
night_sky.resize(0, WINDOW_SIZE[1] * 1.2)
night_sky.sprite.fill((64, 64, 64), special_flags=pygame.BLEND_RGB_SUB)
title_screen.add_child(night_sky)

cs1 = Sprite()
cs1.fill_sprites("traitor/assets/city_background/")
cs1.resize(0, c(250))
cs1.rect.y = center(WINDOW_SIZE[1], cs1.rect.h, (5, 8))

cs2 = Sprite()
cs2.sprite_sheet = cs1.sprite_sheet  # Avoid reloading
cs2.rects = copy.deepcopy(cs1.rects)
cs2.rect.x = cs1.rect.x + cs1.rect.w

city_skyline.add_child(cs1)
city_skyline.add_child(cs2)


def cs_upd():
    self = city_skyline
    for item in (self.children[0], self.children[1]):
        item.rect.x -= c(1)
        if item.rect.x + item.rect.w <= 0:
            item.rect.x += item.rect.w * 2


city_skyline.update = cs_upd

title_screen.add_child(city_skyline)

pavement = Scene()

r1 = Sprite()
r1.fill_sprites("traitor/assets/roads/")
r1.resize(0, WINDOW_SIZE[1] - cs1.rect.y - cs1.rect.h)
r1.sprite_sheet[0] = pygame.transform.scale(
    r1.sprite, (WINDOW_SIZE[0] * 2, WINDOW_SIZE[1] - cs1.rect.y - cs1.rect.h)
)
r1.rects[0] = r1.sprite_sheet[0].get_rect()
r1.rect.y = WINDOW_SIZE[1] - r1.rect.h
r1.sprite.fill((96, 96, 96), special_flags=pygame.BLEND_RGB_SUB)
pavement.add_child(r1)

r2 = Sprite()
r2.sprite_sheet = r1.sprite_sheet  # Avoid reloading
r2.rects = copy.deepcopy(r1.rects)
r2.rect.x = r1.rect.x + r1.rect.w
pavement.add_child(r2)


def pave_upd():
    self = pavement
    for item in (self.children[0], self.children[1]):
        item.rect.x -= c(4)
        if item.rect.x + item.rect.w <= 0:
            item.rect.x += item.rect.w * 2


pavement.update = pave_upd

title_screen.add_child(pavement)

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


rain.frame = 0
rain.update = rain_upd


def rain_render():
    rain.rect.x = 0
    for i in range(7):
        rain.rect.y = 0
        for i in range(4):
            Sprite.render(rain)
            rain.rect.y += rain.rect.h
        rain.rect.x += rain.rect.w


rain.render = rain_render

title_screen.add_child(rain)

new_game_box = Sprite()
new_game_box.fill_sprites("traitor/assets/new_game/")
new_game_box.resize(0, c(40))
new_game_box.rect.x = center(WINDOW_SIZE[0], new_game_box.rect.w)
new_game_box.rect.y = center(WINDOW_SIZE[1], new_game_box.rect.h, (2, 3))
title_screen.add_child(new_game_box)

title_logo = Sprite()
title_logo.sprite_sheet.append(pix_font_xl.render("TRAITOR", True, (255, 153, 0)))
title_logo.rects.append(None)
title_logo.resize(0, WINDOW_SIZE[1] // 3)
title_logo.rect.x = center(WINDOW_SIZE[0], title_logo.rect.w)
title_logo.rect.y = center(WINDOW_SIZE[1], title_logo.rect.h, (1, 3))
logo_shadow = Sprite()
logo_shadow.sprite_sheet.append(pix_font_xl.render("TRAITOR", True, (0, 0, 0, 128)))
logo_shadow.rects.append(None)
logo_shadow.resize(0, WINDOW_SIZE[1] // 3)
logo_shadow.rect.x = title_logo.rect.x
logo_shadow.rect.y = title_logo.rect.y + c(10)

title_screen.add_child(logo_shadow)
title_screen.add_child(title_logo)


# Handle menu options
def title_next(event):
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        pos = pygame.mouse.get_pos()
        # Check if player clicked on the new game box
        if new_game_box.rect.collidepoint(pos):
            title_screen.ret_val = 0


title_screen.handle_input = title_next
