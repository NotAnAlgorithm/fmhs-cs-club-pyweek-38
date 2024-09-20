from . import *


# Basic scene/object-esque structure (?)
# I do not know game dev. I'm winging this
# ;>
class Scene:
    def __init__(self):
        self.guid = uuid4()
        self.parent = None
        self.children = []
        self._ret_val = -1  # Used for communicating to game logic thread
        # -1 - nothing
        # 0 - standard next
        # 1 - end textbox

    def add_child(self, child):
        assert isinstance(child, Scene)
        child.parent = self
        self.children.append(child)

    def rm_child(self, index: int):
        self.children[index].parent = None
        self.children.pop(index)

    def handle_input(self, input: pygame.event):
        pass  # To be overriden!!

    def update(self):
        """
        These are animation updates, not physics updates!
        Please avoid doing a lot of math on these because
        they *will* lag the game!
        ...Famous last words!
        """
        pass  # To be overriden!!!

    def on_display(self):
        """
        Start music, etc.
        Top-down loading, I believe?
        """
        for child in self.children:
            child.on_display()
        pass  # To be overriden!!!

    def repeat_display(self):
        """
        Not as useful!
        """
        for child in self.children:
            child.repeat_display()
        pass  # To be overriden!!!

    def on_death(self):
        """
        When the Scene dies.
        """
        for child in self.children:
            child.on_death()
        pass  # To be overriden!!!

    # Return value decorator
    @property
    def ret_val(self):
        return self._ret_val

    @ret_val.setter
    def ret_val(self, val: int):
        if self.parent is not None:
            self.parent.ret_val = val
        self._ret_val = val


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

    def resize_all(self, scale):
        for i in range(len(self.sprite_sheet)):
            self.resize(i, scale)

    @property
    def location(self):
        return self.rect.x, self.rect.y

    @property
    def rect(self):
        return self.rects[0]  # no dynamic hitboxes just yet

    @property
    def sprite(self):
        return self.sprite_sheet[self.index]
