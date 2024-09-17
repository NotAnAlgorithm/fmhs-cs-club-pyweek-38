from . import *


# Basic scene/object-esque structure (?)
# I do not know game dev. I'm winging this
# ;>
class Scene:
    def __init__(self):
        self.guid = uuid4()
        self.parent = None
        self.children = []

    def add_child(self, child):
        assert isinstance(child, Scene)
        child.parent = self
        self.children.append(child)

    def handle_input(self, input):
        pass  # To be overriden!!

    def update(self):
        """
        These are animation updates, not physics updates!
        Please avoid doing a lot of math on these because
        they *will* lag the game!
        """
        pass  # To be overriden!!!


class Sprite(Scene):
    def __init__(self):
        super().__init__()
        self.rects = []
        self.sprite_sheet = []
        self.index = 0

    def render(self):
        screen.blit(self.sprite, self.rect)  # To be overriden!!!

    def fill_sprites(self, directory):
        for file in sorted(os.listdir(directory)):
            if not (file.endswith(".png") or file.endswith(".jpg")):
                continue
            self.sprite_sheet.append(
                pygame.image.load(os.path.join(directory, file)).convert_alpha()
            )
            self.rects.append(self.sprite_sheet[-1].get_rect())

    def resize(self, index, scale):
        self.sprite_sheet[index] = resize(self.sprite_sheet[index], scale)
        self.rects[index] = self.sprite_sheet[index].get_rect()

    @property
    def location(self):
        return self.rect.x, self.rect.y

    @property
    def rect(self):
        return self.rects[self.index]

    @property
    def sprite(self):
        return self.sprite_sheet[self.index]
