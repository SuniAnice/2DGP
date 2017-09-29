from pico2d import *
import os
import game_framework
import main_state
os.chdir('E:\\2d플\\리소스')
name = "TitleState"
image = None
def enter():
    global image
    open_canvas()
    image = load_image('title.png')
def exit():
    global image
    del(image)
    close_canvas()
def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.quit()
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
                game_framework.change_state(main_state)
def update():
    delay(0.01)
def draw():
    clear_canvas()
    image.draw(400, 300)
    update_canvas()

