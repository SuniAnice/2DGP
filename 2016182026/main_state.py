from pico2d import *
import os
os.chdir('c:\\Users\\lee\\Desktop\\2D')
import title_state
import game_framework
import random
import json_state
class Boy:
    image= None
    LEFT_RUN,RIGHT_RUN,LEFT_STAND,RIGHT_STAND=0,1,2,3
    def __init__(self):
        self.x,self.y=random.randint(100,700),90
        self.frame=random.randint(0,7)
        self.dir=1
        self.run_frames=0
        self.stand_frames=0
        self.state=random.randint(2,3)
        if Boy.image==None:
            Boy.image=load_image('animation_sheet.png')
    def handle_left_run(self):
        self.x-=5
        self.run_frames+=1
        if self.x<0:
            self.x=0
    def handle_left_stand(self):
        self.stand_frames+=1
    def handle_right_run(self):
        self.x+=5
        self.run_frames+=1
        if self.x>800:
            self.x=800
    def handle_right_stand(self):
        self.stand_frames+=1
    def handle_event(self,event):
        if (event.type,event.key)==(SDL_KEYDOWN,SDLK_LEFT):
            if self.state in(self.RIGHT_STAND, self.LEFT_STAND):
                self.state=self.LEFT_RUN
        elif (event.type,event.key)==(SDL_KEYDOWN,SDLK_RIGHT):
            if self.state in (self.RIGHT_STAND,self.LEFT_STAND):
                self.state=self.RIGHT_RUN
        elif (event.type,event.key)==(SDL_KEYUP,SDLK_LEFT):
            if self.state in(self.LEFT_RUN,):
                self.state=self.LEFT_STAND
                self.stand_frames=0
        elif (event.type,event.key)==(SDL_KEYUP,SDLK_RIGHT):
            if self.state in (self.RIGHT_RUN,):
                self.state=self.RIGHT_STAND
                self.stand_frames=0
    handle_state={
            LEFT_RUN:handle_left_run,
            RIGHT_RUN:handle_right_run,
            LEFT_STAND:handle_left_stand,
            RIGHT_STAND:handle_right_stand
    }
    def update(self):
            self.frame=(self.frame+1)%8
            self.handle_state[self.state](self)
            if self.state==self.RIGHT_RUN:
                self.x=min(800,self.x+5)
            elif self.state==self.LEFT_RUN:
                self.x=max(0,self.x-5)

    def draw(self):
        self.image.clip_draw(self.frame*100,self.state*100,100,100,self.x,self.y)


class Grass:
    def __init__(self):
        self.image=load_image('grass.png')

    def draw(self):
        self.image.draw(400,30)

def enter():
    global team,grass,z,s,a
    team=[Boy() for i in range(1000)]
    grass=Grass()
    z=0
    s=str(z)
    a=load_font('Consola.ttf',20)
    json_state.create_team()

def exit():
    global boy,grass,team
    del(team)
    del(grass)


def handle_events():
 global running
 global z
 global s
 global team
 events=get_events()
 for event in events:
  if event.type==SDL_QUIT:
   running=False
  elif event.type==SDL_KEYDOWN:
       if event.key==SDLK_UP:
           z+=1
           if z>999:
               z=999
           s=str(z)
       elif event.key==SDLK_DOWN:
           z-=1
           if z<0:
               z=0
           s=str(z)
       elif event.key==SDLK_ESCAPE:
            game_framework.change_state(title_state)
       else :
            team[z].handle_event(event)
  elif event.type==SDL_KEYUP:
      team[z].handle_event(event)
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
    a.draw(100,50,s,(0,255,0))
    update_canvas()



