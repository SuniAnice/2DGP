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
    global bgm,map,notes,sound,Noteimg,total_time,bgm_isplay,notedata,notecount,score,hero,targetimg

    open_canvas(w=600,h=350,sync=True)

    score = 100

    notecount = 0
    bgm_isplay = False
    bgm = load_music('../bgm/kirby_bgm.mp3')
    bgm.set_volume(96)
    notes = []
    total_time = 0.0

    f = open("../source/kirby.json", "r")
    notedata = json.load(f)
    f.close()

    hero = Kirby()


    Noteimg = load_image('note.png')
    targetimg = load_image('target.png')


    note_create()

    map = Scrollmap()


    sound = load_wav('../bgm/overwatch_kill.wav')
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
    global total_time
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_result.savescore(1, 95)
                game_framework.change_state(game_result)
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
                for note in notes:
                    note.handle_event()
                hero.handle_events(frame_time)

def update(frame_time):
    global bgm,bgm_isplay,notes
    if total_time > 4.0 and bgm_isplay == False:
        bgm.play()
        bgm_isplay = True

    map.update(frame_time)

    hero.update(frame_time)

    for nots in notes:
        nots.update(frame_time)





def draw(frame_time):
    global total_time,notes
    clear_canvas()

    map.draw(frame_time)

    for note in notes:
        note.draw(frame_time)

    hero.draw(frame_time)

    targetimg.draw(400,100)

    update_canvas()

    total_time+=frame_time



class Scrollmap:
    PIXEL_PER_SECOND = 80
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
    def __init__(self):
        self.x = 800.0

    def update(self,frame_time):
        global score
        self.x -=3.33
        if self.x < 0:
            del notes[0]
            score-=1

    def draw(self,frame_time):
        global Noteimg
        Noteimg.draw(self.x,100)

    def handle_event(self):
        global notes
        if self.x >375 and self.x<425 :
            sound.play()
            notes.remove(self)

def note_create():
    global notes,timer,notecount,notedata
    timer = threading.Timer(notedata["data"][notecount],note_create)

    if (notecount != 0):
        a = note()
        notes.append(a)

    notecount+=1

    timer.start()

class Kirby:
    TIME_PER_ACTION = 1
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 8
    def __init__(self):
        self.x = 50
        self.y = 250
        self.image = load_image('wing_kirby.png')

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
    def update(self,frame_time):
        self.total_frames += Kirby.FRAMES_PER_ACTION * Kirby.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % 6

        if self.attacking ==True:
            self.attotalframe += Kirby.FRAMES_PER_ACTION * Kirby.ACTION_PER_TIME * frame_time
            self.attframe = int(self.attotalframe) % 4
            if self.attframe == 3:
                self.attacking = False

    def handle_events(self,frame_time):
        self.attacking = True
        self.attframe = 0
        self.attotalframe = 0




