from pico2d import *
import game_framework
import os
import select_state
os.chdir('../image')
name = "Tutorial"

bgm = None
total_time = 0.0



def enter():
    global bgm
    open_canvas()
    bgm = load_music('../bgm/necro.mp3')
    bgm.set_volume(64)


def exit():
    close_canvas()


def handle_events(frame_time):
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.change_state(select_state)
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
                pass


def update(frame_time):
    pass


def draw(frame_time):
    clear_canvas()


    update_canvas()
    total_time+=frame_time
