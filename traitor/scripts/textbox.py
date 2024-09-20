from .. import *

with open("traitor/assets/dialogue.json", "r") as file:
    dialogue_dump = json.loads(file.read())["dialogue"]

artwork = Sprite()
artwork.fill_sprites("traitor/assets/artwork/")
for i in range(len(artwork.sprite_sheet)):
    artwork.resize(i, c(100))


class Textbox(Sprite):  # not really a sprite, but I need things to recognize it as one
    def __init__(self, dialogue_key: int):
        super().__init__()
        self.dialogue = dialogue_dump[dialogue_key]
        self.name = self.dialogue["name"]
        self.icon = self.dialogue["icon"]
        self.text = self.dialogue["text"]
        self.frame = 0  # to be implemented in post-alpha... animate text, box, more.
        self.progress = -1
        self.limit = 80
        self.art = artwork.sprite_sheet[0]  # for testing only... CHANGE THIS LATER!!

        # internals
        self.text_splice = [
            self.text[i : i + self.limit] for i in range(0, len(self.text), self.limit)
        ]

        self.outer_box = pygame.Surface((WINDOW_SIZE[0], WINDOW_SIZE[1] / 3))
        self.outer_box = self.outer_box, pygame.Rect(
            0,
            WINDOW_SIZE[1] / 3 * 2,
            self.outer_box.get_width(),
            self.outer_box.get_height(),
        )
        self.outer_box[0].set_alpha(224)  # or 192
        self.outer_box[0].fill((0, 0, 0))

        self.art_box = pygame.Rect(c(50), self.outer_box[1][1] - c(100), c(100), c(100))

        self.name_box = pix_font_lg.render(self.name, True, (255, 255, 255)), [
            None,
            self.outer_box[1][1],
        ]
        self.name_box[1][0] = self.art_box.x + center(
            self.art_box.w, self.name_box[0].get_width()
        )

        self.next_line()

    def next_line(self):
        self.progress += 1

        self.text_line_1 = pix_font_sm.render(
            self.text_splice[self.progress], True, (255, 255, 255)
        ), [
            c(25),
            self.outer_box[1][1] + self.name_box[0].get_height() + c(10),
        ]
        if len(self.text_splice) > self.progress + 1:
            self.text_line_2 = pix_font_sm.render(
                self.text_splice[self.progress + 1], True, (255, 255, 255)
            ), [
                self.text_line_1[1][0],
                self.text_line_1[1][1] + self.text_line_1[0].get_height() + c(10),
            ]
        else:
            self.text_line_2 = None

    def update(self):
        super().update()  # not even implemented atm
        pass

    def render(self):  # overriding Sprite's
        screen.blit(*self.outer_box)
        screen.blit(self.art, self.art_box)
        screen.blit(*self.name_box)
        screen.blit(*self.text_line_1)
        if self.text_line_2:
            screen.blit(*self.text_line_2)

    def handle_input(self, event):
        super().handle_input(event)
        pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Check if player clicked on the new game box
            if self.outer_box[1].collidepoint(pos):
                set_cursor(0)
                self.ret_val = 1  # 1 is next textbox
        if event.type == pygame.MOUSEMOTION:
            if self.outer_box[1].collidepoint(pos):
                set_cursor(1)
            else:
                set_cursor(0)
