from pico2d import *
import game_framework
import title_state
import game0_tutorial
import game1_kirby
import os
os.chdir('../image')
name = "SelectState"
bgm = None
def enter():
    global default,left_arrow,right_arrow,select,rotate_sound,bgm,Screen,high
    open_canvas(sync = True)
    select = 0
    Screen = gamescreen()
    default = load_image('whitescreen.png')
    left_arrow = LArrow()
    right_arrow = RArrow()
    bgm = load_music('../bgm/select_screen.mp3')
    high = load_image('HighScore.png')
    bgm.set_volume(64)
    bgm.repeat_play()
    rotate_sound = load_wav('../bgm/rotate.wav')
    rotate_sound.set_volume(48)
def exit():
    global default,left_arrow,right_arrow,Screen,bgm
    bgm.stop()
    del(bgm)
    del(default)
    del(Screen)
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
                right_arrow.SetRed()
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_LEFT):
                if select == 0:
                    select = 4
                else:
                    select-=1
                rotate_sound.play()
                left_arrow.SetRed()
                
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
                Screen.handle_event()
def update(frame_time):
    left_arrow.update()
    right_arrow.update()
def draw(frame_time):
    global select
    clear_canvas()
    default.draw(400,300)

    Screen.draw()

    if select!=0:
        high.draw(300,55)

    left_arrow.draw()
    right_arrow.draw()
        
    
    update_canvas()

class gamescreen:
    def __init__(self):
        self.screen = []
        self.screen.append(load_image('necrodancer.png'))
        self.screen.append(load_image('Kirby Select Scene.png'))
        self.screen.append(load_image('Mario Select Scene.png'))
        self.screen.append(load_image('Overwatch Select Scene.png'))
        self.screen.append(load_image('rhythm_icon.png'))
        self.title = []
        self.title.append(load_image('tutorial-3d-logo.png'))
        self.title.append(load_image('Kirbys_Adventure_Logo.png'))
        self.title.append(load_image('mariotitle.png'))
        self.title.append(load_image('game-logo-overwatch.png'))
        self.title.append(load_image('rhythmtitle.png'))
    def draw(self):
        global select
        image = self.screen[select]
        image2 = self.title[select]
        image.draw(400,300)
        image2.draw(400,500)
    def handle_event(self):
        global select
        if select == 0:
            game_framework.change_state(game0_tutorial)
        elif select == 1:
            game_framework.change_state(game1_kirby)

class LArrow:
    def __init__(self):
        self.image = load_image('Arrow-To-Left_icon.png')
        self.simage = load_image('Arrow-To-Left_icon_Red.png')
        self.frame = 0
        self.redflag = False
    def draw(self):
        if (self.redflag):
            self.simage.draw(70,300)
        else:
            self.image.draw(70,300)
    def update(self):
        if (self.redflag):
            self.frame+=1
            if (self.frame == 20):
                self.frame = 0
                self.redflag = False
    def SetRed(self):
        self.redflag = True
        self.frame = 0

class RArrow:
    def __init__(self):
        self.image = load_image('Arrow-To-icon.png')
        self.simage = load_image('Arrow-To-icon_Red.png')
        self.frame = 0
        self.redflag = False
    def draw(self):
        if (self.redflag):
            self.simage.draw(730,300)
        else:
            self.image.draw(730,300)
    def update(self):
        if (self.redflag):
            self.frame+=1
            if (self.frame == 20):
                self.frame = 0
                self.redflag = False
    def SetRed(self):
        self.redflag = True
        self.frame = 0
            
