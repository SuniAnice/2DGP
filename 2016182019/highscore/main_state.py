from pico2d import *
import game_framework
import main_state
import score_state
import time
import pickle
import json

name = 'main_state'

def enter():
    open_canvas()
def exit():
    close_canvas()
def handle_events():
    global score,timenow
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_MOUSEBUTTONDOWN:
            Gameover(event.x)

def pause():
    close_canvas()
def resume():
    open_canvas()
def update():
    pass
def draw():
    clear_canvas()
    update_canvas()

def Gameover(score):
    entry = score_state.Entry(score,time.asctime(time.localtime()))
    score_state.add(entry)
    game_framework.push_state(score_state)



if __name__ == '__main__':
    game_framework.run(main_state)
