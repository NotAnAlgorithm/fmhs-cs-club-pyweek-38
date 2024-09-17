from . import *

# Avoid using these outside of initial loading of a scene


def c(
    num: int,
):  # Constant. Helps make constants from the scale size 50, which I use to test with.
    return num * (scale / 50)


def center(
    outer, inner, position=(1, 2)
):  # (1,2) == 1/2 as a fraction for screen position
    return outer // position[1] * position[0] - inner // 2


def resize(image, scale):
    return pygame.transform.scale(
        image, (image.get_width() / image.get_height() * scale, scale)
    )


pix_font_lg = pygame.font.Font(
    "traitor/assets/fonts/sh-pinscher/SHPinscher-Regular.otf", int(c(30))
)
pix_font_sm = pygame.font.Font(
    "traitor/assets/fonts/sh-pinscher/SHPinscher-Regular.otf", int(c(25))
)
