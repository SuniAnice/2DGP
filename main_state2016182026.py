from pico2d import *
import os
os.chdir('c:\\Users\\Lenovo\\Desktop\\2D')
import title_state
import game_framework

class Boy:
    def __init__(self):
        self.x,self.y=0,90
        self.frame=0
        self.image=load_image('run_animation.png')

    def update(self):
        self.frame=(self.frame+1)%8
        self.x+=5

    def draw(self):
        self.image.clip_draw(self.frame*100,0,100,100,self.x,self.y)


class Grass:
    def __init__(self):
        self.image=load_image('grass.png')

    def draw(self):
        self.image.draw(400,30)

def enter():
    global boy,grass
    boy=Boy()
    grass=Grass()

def exit():
    global boy,grass
    del(boy)
    del(grass)

def handle_events():
    events=get_events()
    for event in events:
        if event.type ==SDL_QUIT:
            game_framework.quit()
        elif event.type==SDL_KEYDOWN and event.key==SDLK_ESCAPE:
            game_framework.change_state(title_state)

def update():
    boy.update()

def draw():
    clear_canvas()
    grass.draw()
    boy.draw()
    update_canvas()
    
