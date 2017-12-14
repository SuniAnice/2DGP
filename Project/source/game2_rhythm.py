from pico2d import *
import game_framework
import os
import threading
import select_state
import game_result
import json
os.chdir('../image')
name = "Rhythm"




def enter():
    global bgm,map,notes,sound,Noteimg,total_time,bgm_isplay,notedata,notecount,score,target,hero

    open_canvas(sync=True)

    score = 100

    notecount = 0
    bgm_isplay = False
    bgm = load_music('../bgm/rhythm.mp3')
    bgm.set_volume(64)
    notes = []
    total_time = 0.0

    f = open("../source/Kirby.json", "r")
    notedata = json.load(f)
    f.close()

    hero = Fighter()

    Noteimg = load_image('target.png')

    target = judgenote()

    note_create()

    map = Scrollmap()


    sound = load_wav('../bgm/맞는소리.wav')
    sound.set_volume(64)



def exit():
    global timer,bgm,sound,map,notes
    timer.cancel()
    bgm.stop()
    del(bgm)
    del(sound)
    del(map)
    del(notes)


    close_canvas()



def handle_events(frame_time):
    global total_time,score
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_result.savescore(2, clamp(0,score,100))
                game_framework.change_state(game_result)
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
                for note in notes:
                    note.handle_event()


def update(frame_time):
    global bgm,bgm_isplay,notes
    if total_time > 2.0 and bgm_isplay == False:
        bgm.play()
        bgm_isplay = True

    map.update(frame_time)

    hero.update(frame_time)

    target.update(frame_time)


    for nots in notes:
        nots.update(frame_time)

    if total_time > 134.0:
        game_result.savescore(2, clamp(0,score,100))
        game_framework.change_state(game_result)



def draw(frame_time):
    global total_time,notes
    clear_canvas()

    map.draw(frame_time)

    for note in notes:
        note.draw(frame_time)


    hero.draw(frame_time)

    target.draw(frame_time)



    update_canvas()

    total_time+=frame_time



class Scrollmap:
    PIXEL_PER_SECOND = 120
    def __init__(self):
        self.x = 0
        self.image = load_image('rhythm_background.png')

    def draw(self,frame_time):
        x = int(self.x)
        w = min(self.image.w-x,800)
        self.image.clip_draw_to_origin(x, 0, w, 600, 0, 0)
        self.image.clip_draw_to_origin(0, 0, 800-w, 600, w, 0)

    def update(self,frame_time):
        self.x = (self.x + frame_time * self.PIXEL_PER_SECOND) % self.image.w

class note:
    SPEED_PER_SECOND = 200
    def __init__(self):
        self.x = 600.0
        self.frame = 0

    def update(self,frame_time):
        global score
        self.x -= note.SPEED_PER_SECOND * frame_time
        if self.x < 130:
            del notes[0]
            score-=1


    def draw(self,frame_time):
        global Noteimg
        Noteimg.draw(self.x,250)

    def handle_event(self):
        global notes,target
        if self.x >170 and self.x<230 :
            sound.play()
            notes.remove(self)
            target.effecton()

class Fighter:
    def __init__(self):
        self.x = 100
        self.y = 50
        self.frame = 0
        self.image = load_image('rhythm_sprite.png')

    def draw(self,frame_time):
        self.image.clip_draw(450,0,150,150,self.x,self.y)

    def update(self,frame_time):
        pass


def note_create():
    global notes,timer,notecount,notedata
    if (notecount<=len(notedata["data"])-1):

        timer = threading.Timer(notedata["data"][notecount],note_create)

        if (notecount != 0):
            a = note()
            notes.append(a)

        notecount+=1
        timer.start()


class judgenote:
    TIME_PER_ACTION = 1
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 12
    def __init__(self):
        self.x = 200
        self.y = 200
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






