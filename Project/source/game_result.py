from pico2d import *
import game_framework
import os
import select_state
import time
import json
os.chdir('../image')
name = "result"
string = ""




def savescore(gamecode,score):
    global result
    result = score
    f= open('../source/highscore.json','r')
    scores = json.load(f)
    f.close()
    if gamecode == 1:
        if (scores["game1"] < result):
            f = open('../source/highscore.json','w')
            scores["game1"] = result
            json.dump(scores,f)
            f.close()
    elif gamecode == 2:
        if (scores["game2"] < result):
            f = open('../source/highscore.json','w')
            scores["game2"] = result
            json.dump(scores,f)
            f.close()
    elif gamecode == 3:
        if (scores["game3"] < result):
            f = open('../source/highscore.json','w')
            scores["game3"] = result
            json.dump(scores,f)
            f.close()
    if gamecode == 4:
        if (scores["game4"] < result):
            f = open('../source/highscore.json','w')
            scores["game4"] = result
            json.dump(scores,f)
            f.close()




def enter():
    global bgm,sound,total_time,screen,bgm_isplay,result_img,sound,sound_isplay,font
    open_canvas()


    font = load_font('HUSimple.ttf',50)

    bgm = load_music('../bgm/result.mp3')
    bgm.set_volume(64)
    total_time = 0.0
    bgm_isplay = False
    sound_isplay = False

    screen = load_image('whitescreen.png')

    if result > 80:
        result_img = load_image('참_잘했어요.png')
        sound = load_wav('../bgm/clear.wav')
        sound.set_volume(32)
    else:
        result_img = load_image('참_망했어요.png')
        sound = load_wav('../bgm/failed.wav')
        sound.set_volume(32)











def exit():
    global bgm,screen,sound
    bgm.stop()
    del(bgm)
    del(screen)
    del(sound)

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

def update(frame_time):
    global bgm,notes,bgm_isplay

    if total_time > 0.5 and bgm_isplay == False:
        bgm.play()
        bgm_isplay = True








def draw(frame_time):
    global total_time,sound_isplay,result
    clear_canvas()

    string = str(result) + "점"


    screen.draw(400,300)

    if (total_time > 2.5):
        result_img.draw(400,300)

        font.draw(350,80,string,(0,0,255))
        if sound_isplay == False:
            sound.play()
            sound_isplay = True






    update_canvas()

    total_time+=frame_time



