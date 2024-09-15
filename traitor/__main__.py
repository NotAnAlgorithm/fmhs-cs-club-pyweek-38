from . import *

# Main loop
def main():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                pass

        pygame.display.update()
        fps_timer.tick(60) # 60 fps cap

if __name__ == '__main__':
    main()
