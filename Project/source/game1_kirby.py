from pico2d import *
import game_framework
import os
import threading
import select_state
import game_result
os.chdir('../image')
name = "Kirby"





def enter():
    global bgm,map,notes,sound,Noteimg,total_time,bgm_isplay
    open_canvas(w=600,h=350,sync=True)

    bgm_isplay = False
    bgm = load_music('../bgm/kirby_bgm.mp3')
    bgm.set_volume(96)
    notes = []
    total_time = 0.0

    Noteimg = load_image('note.png')


    note_create()
    #a = note()

    map = Scrollmap()


    sound = load_wav('../bgm/overwatch_kill.wav')
    sound.set_volume(64)






def exit():
    global timer,bgm,sound,map
    timer.cancel()
    bgm.stop()
    del(bgm)
    del(sound)
    del(map)


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

def update(frame_time):
    global bgm,bgm_isplay,notes
    if total_time > 2.0 and bgm_isplay == False:
        bgm.play()
        bgm_isplay = True

    map.update(frame_time)

    for nots in notes:
        nots.update(frame_time)





def draw(frame_time):
    global total_time,notes
    clear_canvas()

    map.draw(frame_time)






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
        self.x = self.x + frame_time * self.PIXEL_PER_SECOND % self.image.w

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

def note_create():
    global notes,timer
    timer = threading.Timer(0.5,note_create)

    a = note()
    notes.append(a)

    timer.start()


class judge:
    pass
