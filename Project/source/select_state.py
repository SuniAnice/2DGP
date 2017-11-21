from pico2d import *
import game_framework
import title_state
import game0_tutorial
import os
os.chdir('../image')
name = "SelectState"
bgm = None
def enter():
    global default,left_arrow,right_arrow,select,rotate_sound,bgm,Screen
    open_canvas()
    select = 0
    Screen = gamescreen()
    default = load_image('whitescreen.png')
    left_arrow = load_image('Arrow-To-Left_icon.png')
    right_arrow = load_image('Arrow-To-icon.png')
    bgm = load_music('../bgm/select_screen.mp3')
    bgm.set_volume(64)
    bgm.repeat_play()
    rotate_sound = load_wav('../bgm/rotate.wav')
    rotate_sound.set_volume(48)
def exit():
    global default,left_arrow,right_arrow,Screen
    del(default)
    #del(Screen)
    del(left_arrow)
    del(right_arrow)
    close_canvas()
def handle_events(frame_time):
    global select,rotate_sound
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.change_state(title_state)
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_RIGHT):
                if select == 4:
                    select = 0
                else:
                    select+=1
                rotate_sound.play()
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_LEFT):
                if select == 0:
                    select = 4
                else:
                    select-=1
                rotate_sound.play()
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
                Screen.handle_event()
def update(frame_time):
    pass
def draw(frame_time):
    global select
    clear_canvas()
    default.draw(400,300)

    Screen.draw()

    left_arrow.draw(70,300)
    right_arrow.draw(730,300)
        
    
    update_canvas()

class gamescreen:
    def __init__(self):
        self.screen = []
        self.screen.append(load_image('necrodancer.png'))
        self.screen.append(load_image('Kirby Select Scene.png'))
        self.screen.append(load_image('Mario Select Scene.png'))
        self.screen.append(load_image('Overwatch Select Scene.png'))
        self.screen.append(load_image('Rhythm Select Scene.png'))
    def draw(self):
        global select
        image = self.screen[select]
        image.draw(400,300)
    def handle_event(self):
        global select
        if select == 0:
            game_framework.change_state(game0_tutorial)
