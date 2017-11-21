from pico2d import *
import game_framework
import select_state
import os
os.chdir('../image')
name = "TitleState"
image = None
bgm = None
def enter():
    global image,bgm
    open_canvas()
    image = load_image('title.png')
    bgm = load_music('../bgm/title.mp3')
    bgm.set_volume(64)
    bgm.repeat_play()
def exit():
    global image
    del(image)
    close_canvas()
def handle_events(frame_time):
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.quit()
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
                game_framework.change_state(select_state)
def update(frame_time):
    pass
def draw(frame_time):
    clear_canvas()
    image.draw(400, 300)
    update_canvas()

