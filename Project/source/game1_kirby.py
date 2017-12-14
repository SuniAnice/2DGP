from pico2d import *
import game_framework
import os
import threading
import select_state
import game_result
import json
os.chdir('../image')
name = "Kirby"




def enter():
    global bgm,map,notes,sound,Noteimg,total_time,bgm_isplay,notedata,notecount,score,hero,target,hitsound

    open_canvas(w=600,h=350,sync=True)

    score = 100

    notecount = 0
    bgm_isplay = False
    bgm = load_music('../bgm/kirby_bgm.mp3')
    bgm.set_volume(96)
    notes = []
    total_time = 0.0

    f = open("../source/Kirby.json", "r")
    notedata = json.load(f)
    f.close()

    hero = Kirby()

    Noteimg = load_image('enemy_sprtie.png')

    target = judgenote()

    note_create()

    map = Scrollmap()

    hitsound = load_wav('../bgm/hit.wav')
    hitsound.set_volume(64)


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
                game_result.savescore(1, clamp(0,score,100))
                game_framework.change_state(game_result)
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
                for note in notes:
                    note.handle_event()
                hero.handle_events(frame_time)

def update(frame_time):
    global bgm,bgm_isplay,notes
    if total_time > 3.5 and bgm_isplay == False:
        bgm.play()
        bgm_isplay = True

    map.update(frame_time)

    target.update(frame_time)

    hero.update(frame_time)

    for nots in notes:
        nots.update(frame_time)

    if total_time > 134.0:
        game_result.savescore(1, clamp(0,score,100))
        game_framework.change_state(game_result)



def draw(frame_time):
    global total_time,notes
    clear_canvas()

    map.draw(frame_time)

    for note in notes:
        note.draw(frame_time)



    target.draw(frame_time)

    hero.draw(frame_time)

    update_canvas()

    total_time+=frame_time



class Scrollmap:
    PIXEL_PER_SECOND = 120
    def __init__(self):
        self.x = 0
        self.image = load_image('kirby_map.png')

    def draw(self,frame_time):
        x = int(self.x)
        w = min(self.image.w-x,600)
        self.image.clip_draw_to_origin(x, 350, w, 350, 0, 0)
        self.image.clip_draw_to_origin(0, 350, 600-w, 350, w, 0)

    def update(self,frame_time):
        self.x = (self.x + frame_time * self.PIXEL_PER_SECOND) % self.image.w

class note:
    SPEED_PER_SECOND = 200
    def __init__(self):
        self.x = 600.0
        self.frame = 0
        self.total_frame = 0

    def update(self,frame_time):
        global score
        self.x -= note.SPEED_PER_SECOND * frame_time
        if self.x < 130:
            del notes[0]
            score-=1
            hero.effecton()
            hitsound.play()
        self.total_frame += Kirby.FRAMES_PER_ACTION * Kirby.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frame) % 7

    def draw(self,frame_time):
        global Noteimg
        Noteimg.clip_draw(self.frame*100,0,100,100,self.x,200)

    def handle_event(self):
        global notes,target
        if self.x >170 and self.x<230 :
            sound.play()
            notes.remove(self)
            target.effecton()

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

class Kirby:
    TIME_PER_ACTION = 1
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 8
    def __init__(self):
        self.x = 130
        self.y = 200
        self.image = load_image('wing_kirby.png')

        self.atteffect = load_image('attack_motion.png')



        self.effect = load_image('Effect_sprite.png')

        self.effectflag = False
        self.efframe = 0
        self.total_efframe = 0

        self.frame = 0
        self.total_frames = 0

        self.attacking = False
        self.attframe = 0
        self.attotalframe = 0

    def draw(self,frame_time):
        if self.attacking == False:
            self.image.clip_draw(37+self.frame*75,195,75,91, self.x,self.y)
        else:
            self.image.clip_draw(80 + self.attframe * 75, 20, 75, 91, self.x, self.y)
            self.atteffect.clip_draw(75 * (self.attframe-1),0,75,91,target.x,self.y)

        if self.effectflag == True:
            self.effect.clip_draw(75*self.frame,0,75,75,self.x,self.y)

    def update(self,frame_time):
        self.total_frames += Kirby.FRAMES_PER_ACTION * Kirby.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % 6

        if self.attacking ==True:
            self.attotalframe += Kirby.FRAMES_PER_ACTION * Kirby.ACTION_PER_TIME * frame_time
            self.attframe = int(self.attotalframe) % 4
            if self.attframe == 3:
                self.attacking = False

        if self.effectflag == True:
            self.total_efframe += judgenote.FRAMES_PER_ACTION * judgenote.ACTION_PER_TIME * frame_time
            self.efframe = int(self.total_efframe) % 9
            if (self.efframe == 8):
                self.effectflag = False

    def handle_events(self,frame_time):
        self.attacking = True
        self.attframe = 0
        self.attotalframe = 0

    def effecton(self):
        self.effectflag = True
        self.efframe = 0
        self.total_efframe = 0




