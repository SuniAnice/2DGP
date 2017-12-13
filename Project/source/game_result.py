from pico2d import *
import game_framework
import os
import select_state
os.chdir('../image')
name = "result"


def savescore(gamecode,score):
    global result
    result = score


def enter():
    global bgm,sound,total_time,screen,bgm_isplay,result_img
    open_canvas()

    bgm = load_music('../bgm/result.mp3')
    bgm.set_volume(64)
    total_time = 0.0
    bgm_isplay = False

    screen = load_image('whitescreen.png')

    if result > 80:
        result_img = load_image('참_잘했어요.png')
    else:
        result_img = load_image('참_망했어요.png')











def exit():
    global bgm,screen
    bgm.stop()
    del(bgm)
    del(screen)

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

    if total_time > 1.0 and bgm_isplay == False:
        bgm.play()
        bgm_isplay = True








def draw(frame_time):
    global total_time
    clear_canvas()


    screen.draw(400,300)

    result_img.draw(400,300)




    update_canvas()

    total_time+=frame_time



