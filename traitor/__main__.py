from . import *


def loop_eternally(parent: Scene, function: callable):
    function(parent)
    for scene in parent.children:
        if len(scene.children) > 0:
            loop_eternally(scene, function)
        else:
            function(scene)


def draw_sprites(scene: Scene):
    if isinstance(scene, Sprite):
        scene.render()


def call_physics(scene: Scene):
    scene.physics()


class Input:
    def __init__(self, parameter):
        self.parameter = parameter

    def handle_inputs(self, scene: Scene):
        scene.handle_input(self.parameter)


# Main loop
def main():
    current_scene = title_screen  # ???

    while True:
        screen.fill((255, 255, 255))  # Clear

        # Render
        loop_eternally(current_scene, draw_sprites)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            loop_eternally(current_scene, Input(event).handle_inputs)

        loop_eternally(current_scene, call_physics)

        pygame.display.update()
        fps_timer.tick(60)  # 60 fps cap


if __name__ == "__main__":
    main()
