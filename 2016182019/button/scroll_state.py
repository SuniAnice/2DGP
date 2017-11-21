from pico2d import *

import game_framework


from boy import FreeBoy as Boy # import Boy class from boy.py
from background import FixedBackground as Background
import ui


name = "scroll_state"

boy = None
background = None

def create_world():
    global boy, background,button,button2
    boy = Boy()
    button = ui.Button('시작버튼.png','종료버튼.png',200,300)
    button.onClick = onBtnInsta
    button.text = "OK"
    button2 = ui.Button('종료버튼.png','시작버튼.png', 600, 300)
    button2.onClick = onBtnTwt
    button2.text = "CANCEL"
    background = Background()

    background.set_center_object(boy)
    boy.set_background(background)

def onBtnInsta():
    print('a')

def onBtnTwt():
    print('b')

def destroy_world():
    global boy, background
    del(boy)
    del(background)


def enter():
    open_canvas(800, 600)
    game_framework.reset_time()
    create_world()


def exit():
    destroy_world()
    close_canvas()


def pause():
    pass

def resume():
    pass


def handle_events(frame_time):
    global button,button2
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.quit()
            else:
                boy.handle_event(event)
                background.handle_event(event)
                ui.handle_event(event)
                #button.handle_event(event)
                #button2.handle_event(event)



def update(frame_time):
    boy.update(frame_time)
    background.update(frame_time)



def draw(frame_time):
    global button,button2
    clear_canvas()
    background.draw()
    boy.draw()
    #button.draw()
    #button2.draw()
    ui.draw()
    update_canvas()






