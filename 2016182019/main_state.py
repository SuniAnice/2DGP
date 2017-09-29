from pico2d import *
import os
import game_framework
import random
import title_state
def enter():
    global team, grass,select
    open_canvas()
    team = [Boy() for i in range(11)]
    select = 0
    grass = Grass()
def exit():
    global team, grass
    del(team)
    del(grass)
    close_canvas()
def handle_events():
    global select
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_state(title_state)
        elif event.type == SDL_MOUSEMOTION:
            team[select].x,team[select].y = event.x,600-event.y
        elif event.type == SDL_KEYDOWN and event.key == SDLK_F1:
            select = 0
        elif event.type == SDL_KEYDOWN and event.key == SDLK_F2:
            select = 1
        elif event.type == SDL_KEYDOWN and event.key == SDLK_F3:
            select = 2
        elif event.type == SDL_KEYDOWN and event.key == SDLK_F4:
            select = 3
        elif event.type == SDL_KEYDOWN and event.key == SDLK_F5:
            select = 4
        elif event.type == SDL_KEYDOWN and event.key == SDLK_F6:
            select = 5
        elif event.type == SDL_KEYDOWN and event.key == SDLK_F7:
            select = 6
        elif event.type == SDL_KEYDOWN and event.key == SDLK_F8:
            select = 7
        elif event.type == SDL_KEYDOWN and event.key == SDLK_F9:
            select = 8
        elif event.type == SDL_KEYDOWN and event.key == SDLK_F10:
            select = 9
        elif event.type == SDL_KEYDOWN and event.key == SDLK_F11:
            select = 10
def update():
    for boy in team:
        boy.update()
        boy.x+=2
    delay(0.05)
def draw():
    clear_canvas()
    grass.draw()
    for boy in team:
        boy.draw()
    update_canvas()
class Grass:
    def __init__(self):
        self.image = load_image('grass.png')
    def draw(self):
        self.image.draw(400, 30)
class Boy:
    def __init__(self):
        self.x, self.y = random.randint(100,700),90
        self.frame = random.randint(0, 7)
        self.image = load_image('run_animation.png')
    def update(self):
        self.frame = (self.frame + 1) % 8
    def draw(self):
        self.image.clip_draw(self.frame*100, 0, 100, 100, self.x, self.y)
