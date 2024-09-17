from .. import *

game_start = Scene()
internal_scene = None

def update_scene(): # Sends an update to the main thread
    global internal_scene
    q.put(internal_scene)
    update_event.set()
    print('Scene update!')

def wait_update(): # Waits for the next scene
    global internal_scene
    past_scene = internal_scene.guid
    while past_scene == internal_scene.guid:
        pass

def game_logic():
    global internal_scene
    internal_scene = title_screen

    def title_next(event):
        global internal_scene
        if event.type == KEYDOWN:
            internal_scene = Textbox(0)
    title_screen.handle_input = title_next

    update_scene()

    wait_update()
    update_scene()

