from .. import *

credits_scene = Scene()

c1 = Sprite()
c1.sprite_sheet.append(pix_font_xl.render("UNFINISHED", True, (255, 153, 0)))
c1.rects.append(None)
c1.resize(0, WINDOW_SIZE[1] // 3)
c1.rect.x = center(WINDOW_SIZE[0], c1.rect.w)
c1.rect.y = center(WINDOW_SIZE[1], c1.rect.h, (1, 3))

credits_scene.add_child(c1)
