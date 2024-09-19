from . import *


def draw_sprites(scene: Scene):
    if isinstance(scene, Sprite):
        scene.render()


def call_update(scene: Scene):
    scene.update()


class Input:
    def __init__(self, parameter):
        self.parameter = parameter

    def handle_inputs(self, scene: Scene):
        scene.handle_input(self.parameter)


# Main loop
def main():
    current_scene = None

    thread = threading.Thread(target=game_logic, args=(), daemon=True)
    thread.start()

    while True:
        screen.fill((0, 0, 0))  # Clear

        if update_event.isSet():
            update_event.clear()
            try:  # Grab updated scene from logic thread
                scene = q.get()
                if isinstance(scene, Scene):
                    current_scene = scene
            except:
                pass

        if current_scene is not None:
            # Render
            loop_eternally(current_scene, draw_sprites)

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                loop_eternally(current_scene, Input(event).handle_inputs)

            loop_eternally(current_scene, call_update)
        else:
            print("Game could be freezing. I don't know")

        pygame.display.update()
        fps_timer.tick(60)  # 60 fps cap


if __name__ == "__main__":
    main()
