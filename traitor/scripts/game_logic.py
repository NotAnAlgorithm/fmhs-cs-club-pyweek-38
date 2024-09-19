from .. import *

game_start = Scene()
internal_scene = None


def update_scene():  # Sends an update to the main thread
    global internal_scene
    q.put(internal_scene)
    update_event.set()
    print("Scene update!")


def wait_return():  # Waits for the next scene
    global internal_scene
    while internal_scene.ret_val == -1:
        pass
    val = internal_scene.ret_val
    internal_scene.ret_val = -1
    return val


def game_logic():
    global internal_scene

    while True:
        internal_scene = title_screen
        update_scene()

        title_choice = wait_return()
        match title_choice:
            case 0:
                internal_scene = World()
                update_scene()
                wait_return()
            case -1:
                continue
            case _:
                raise os._exit(1)
        update_scene()
