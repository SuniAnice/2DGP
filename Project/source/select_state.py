from pico2d import *
import game_framework
import title_state
import os
os.chdir('../image')
name = "SelectState"
def enter():
    global game1,game2,game3,game4,default,left_arrow,right_arrow,select
    open_canvas()
    select = 1
    default = load_image('whitescreen.png')
    game1 = load_image('Kirby Select Scene.png')
    game2 = load_image('Mario Select Scene.png')
    game3 = load_image('Overwatch Select Scene.png')
    game4 = load_image('Rhythm Select Scene.png')
    left_arrow = load_image('Arrow-To-Left_icon.png')
    right_arrow = load_image('Arrow-To-icon.png')
def exit():
    global game1,game2,game3,game4,default,left_arrow,right_arrow
    del(default)
    del(game1)
    del(game2)
    del(game3)
    del(game4)
    del(left_arrow)
    del(right_arrow)
    close_canvas()
def handle_events():
    global select
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.change_state(title_state)
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_RIGHT):
                if select == 4:
                    select = 1
                else:
                    select+=1
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_LEFT):
                if select == 1:
                    select = 4
                else:
                    select-=1
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
                pass
def update():
    delay(0.01)
def draw():
    global select
    clear_canvas()
    default.draw(400,300)
    if select == 1:
        game1.draw(400,300)
    elif select == 2:
        game2.draw(400,300)
    elif select == 3:
        game3.draw(400,300)
    elif select == 4:
        game4.draw(400,300)

    left_arrow.draw(70,300)
    right_arrow.draw(730,300)
        
    
    update_canvas()
