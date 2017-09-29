from pico2d import *
import os
os.chdir('c:\\Users\\Lenovo\\Desktop\\2D')
import title_state
import game_framework

class Boy:
    def __init__(self):
        self.x,self.y=0,90
        self.frame=0
        self.image=load_image('run_animation.png')

    def update(self):
        self.frame=(self.frame+1)%8
        self.x+=5

    def draw(self):
        self.image.clip_draw(self.frame*100,0,100,100,self.x,self.y)


class Grass:
    def __init__(self):
        self.image=load_image('grass.png')

    def draw(self):
        self.image.draw(400,30)

def enter():
    global team,grass,z
    team=[Boy() for i in range(11)]
    grass=Grass()
    z=0


def exit():
    global boy,grass,team
    del(team)
    del(grass)

def handle_events():
 global running
 global z
 events=get_events()
 for event in events:
  if event.type==SDL_QUIT:
   running=False
  elif event.type==SDL_KEYDOWN and event.key==SDLK_1:
    z=1
  elif event.type==SDL_KEYDOWN and event.key==SDLK_2:
    z=2
  elif event.type==SDL_KEYDOWN and event.key==SDLK_3:
    z=3
  elif event.type==SDL_KEYDOWN and event.key==SDLK_4:
    z=4
  elif event.type==SDL_KEYDOWN and event.key==SDLK_5:
    z=5
  elif event.type==SDL_KEYDOWN and event.key==SDLK_6:
    z=6
  elif event.type==SDL_KEYDOWN and event.key==SDLK_7:
    z=7
  elif event.type==SDL_KEYDOWN and event.key==SDLK_8:
    z=8
  elif event.type==SDL_KEYDOWN and event.key==SDLK_9:
    z=9
  elif event.type==SDL_KEYDOWN and event.key==SDLK_0:
    z=0
  elif event.type==SDL_KEYDOWN and event.key==SDLK_RIGHT:
    team[z].x+=10
  elif event.type==SDL_KEYDOWN and event.key==SDLK_LEFT:
    team[z].x-=10
  elif event.type==SDL_KEYDOWN and event.key==SDLK_ESCAPE:
    game_framework.change_state(title_state)
  elif event.type==SDL_MOUSEMOTION:
   team[z].x,team[z].y=event.x,600-event.y

def update():
    for boy in team:
        boy.update()
    delay(0.05)

def draw():
    clear_canvas()
    grass.draw()
    for boy in team:
        boy.draw()
    update_canvas()
    
