from pico2d import *
import game_framework
import os
import threading
import select_state
os.chdir('../image')
name = "Tutorial"





def enter():
    global bgm,hero,mob,map,notes,sound,Noteimg,total_time,notes,bgm_isplay,target
    open_canvas(sync=True)

    bgm_isplay = False
    bgm = load_music('../bgm/necro.mp3')
    bgm.set_volume(64)
    notes = []
    total_time = 0.0

    Noteimg = load_image('note.png')

    target = judgenote()

    note_create()


    sound = load_wav('../bgm/overwatch_kill.wav')
    sound.set_volume(64)

    map = load_image('necrodancer_map.png')

    hero = Hero()

    mob = skeleton()


def exit():
    global map,mob,hero,Noteimg,notes,timer
    timer.cancel()
    del(Noteimg)
    del(map)
    del(hero)
    del(mob)
    del(notes)
    close_canvas()



def handle_events(frame_time):
    global total_time
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.change_state(select_state)
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
                for note in notes:
                    note.handle_event()

def update(frame_time):
    global bgm,bgm_isplay,notes
    if total_time > 2.0 and bgm_isplay == False:
        bgm.play()
        bgm_isplay = True

    target.update(frame_time)


    for nots in notes:
        nots.update(frame_time)

    mob.update(frame_time)
    hero.update(frame_time)



def draw(frame_time):
    global total_time,mob,map,hero,notes
    clear_canvas()

    map.draw(400, 300)

    target.draw(frame_time)

    for nots in notes:
        nots.draw(frame_time)


    hero.draw(frame_time)


    mob.draw(frame_time)

    update_canvas()
    total_time+=frame_time

class skeleton:
    TIME_PER_ACTION = 1
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 8
    def __init__(self):
        self.image = load_image('스켈레톤.png')
        self.frame = 0
        self.total_frames = 0
    def update(self,frame_time):
        global notes
        self.total_frames += skeleton.FRAMES_PER_ACTION * skeleton.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % 15
    def draw(self,frame_time):
        self.image.clip_draw(self.frame * 97 ,0,100,100,500,300)

class Hero:
    TIME_PER_ACTION = 1
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 8
    def __init__(self):
        self.image = load_image('necrodancer_sprite.png')
        self.frame = 0
        self.total_frames = 0
    def update(self,frame_time):
        global notes
        self.total_frames += Hero.FRAMES_PER_ACTION * Hero.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % 4
    def draw(self,frame_time):
        self.image.clip_draw(self.frame * 105 ,0,100,100,320,300)

class note:
    def __init__(self):
        self.x = 800.0

    def update(self,frame_time):
        self.x -=3.33
        if self.x < 0:
            del notes[0]

    def draw(self,frame_time):
        global Noteimg
        Noteimg.draw(self.x,500)

    def handle_event(self):
        global notes
        if self.x >350 and self.x<450:
            sound.play()
            notes.remove(self)
            target.effecton()

def note_create():
    global notes,timer
    timer = threading.Timer(0.5,note_create)

    a = note()
    notes.append(a)

    timer.start()


class judgenote:
    TIME_PER_ACTION = 1
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 12
    def __init__(self):
        self.x = 400
        self.y = 500
        self.image = load_image('target.png')
        self.effect = load_image('Effect_sprite.png')
        self.effectflag = False
        self.frame = 0
        self.total_frame = 0
    def draw(self,frame_time):
        self.image.draw(self.x,self.y)
        if self.effectflag == True:
            self.effect.clip_draw(75*self.frame,0,75,75,self.x,self.y)
    def update(self,frame_time):
        self.total_frame += judgenote.FRAMES_PER_ACTION * judgenote.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frame) % 9
        if (self.frame == 8):
            self.effectflag = False
    def effecton(self):
        self.effectflag = True
        self.frame = 0
        self.total_frame = 0
