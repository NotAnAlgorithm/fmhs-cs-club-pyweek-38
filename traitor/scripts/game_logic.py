from .. import *

game_start = Scene()
internal_scene = None


def update_scene():  # Sends an update to the main thread
    global internal_scene
    q.put(internal_scene)
    update_event.set()
    print("Scene update!")


def wait_return(update: bool = True):  # Waits for the next scene
    if update:
        update_scene()
    global internal_scene
    while internal_scene.ret_val == -1:
        pass
    val = internal_scene.ret_val
    internal_scene.ret_val = -1
    return val


def game_logic():
    global internal_scene

    while True:
        title_logic()
        update_scene()


def title_logic():
    global internal_scene
    internal_scene = title_screen

    title_choice = wait_return()
    match title_choice:
        case 0:
            beginning_cutscene()
            playable_world()
            wait_return()
            # unknown...
            os._exit(0)
        case 1:
            internal_scene = credits_scene
            wait_return()
            title_logic()
        case _:
            raise os._exit(1)


def beginning_cutscene():
    global internal_scene

    internal_scene.rm_child(-1)
    internal_scene.rm_child(-1)
    internal_scene.rm_child(-1)
    internal_scene.rm_child(-1)
    internal_scene.add_child(Textbox(0))
    wait_return()
    internal_scene.rm_child(-1)
    internal_scene.add_child(Textbox(1))
    wait_return()
    internal_scene.rm_child(-1)
    internal_scene.add_child(Textbox(3))
    wait_return()
    internal_scene.rm_child(-1)
    internal_scene.add_child(Textbox(4))
    wait_return()
    internal_scene.rm_child(-1)
    internal_scene.add_child(Textbox(5))
    wait_return()
    internal_scene.rm_child(-1)
    internal_scene.add_child(Textbox(6))
    wait_return()
    internal_scene.rm_child(-1)
    internal_scene.add_child(Textbox(7))
    wait_return()
    internal_scene.rm_child(-1)
    internal_scene.add_child(Textbox(8))
    wait_return()
    internal_scene.rm_child(-1)
    internal_scene.add_child(Textbox(9))
    wait_return()
    internal_scene.car_door_close()


def playable_world():
    global internal_scene
    ret_val = internal_scene.ret_val
    while ret_val != 0:
        internal_scene = Outside()
        ret_val = wait_return()

        match ret_val:
            case 3:  # inner base
                pygame.mixer.music.load("traitor/assets/sounds/espionage.ogg")
                pygame.mixer.music.set_volume(1)
                pygame.mixer.music.play(-1)
            case _:
                print("who knows")
