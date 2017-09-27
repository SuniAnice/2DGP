from pico2d import *
import os
os.chdir('c:\\Users\\Lenovo\\Desktop\\2D')
import main_state
import game_framework

name="Titlestate"
image=None

def enter():
    global image
    image=load_image('title.png')

def exit():
    global image
    del(image)

def handle_events():
    events=get_events()
    for event in events:
        if event.type==SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type,event.key)==(SDL_KEYDOWN,SDLK_ESCAPE):
                game_framework.quit()
            elif (event.type,event.key)==(SDL_KEYDOWN,SDLK_SPACE):
                game_framework.change_state(main_state)


def draw():
    clear_canvas()
    image.draw(400,300)
    update_canvas()


        
def update():
    pass
def resume():
    pass
