from pico2d import *
import game_framework
import random
import time
import title_state
import json_player
import background
def enter():
    global team, grass,select,font,frame_time,maxplayer,back
    open_canvas()
    Boy.image = None
    Grass.image = None
    background.Background.image = None
    frame_time = 0.01
    team,maxplayer = json_player.create_team()
    select = 0
    grass = Grass()
    back = background.Background()
    font = load_font('Consola.ttf',25)
def exit():
    global team, grass,font,back
    del(grass)
    del(font)
    del(team)
    del(back)
    close_canvas()
def handle_events():
    global select,Boy,maxplayer
    events = get_events()
    for event in events:
        back.handle_events(event)
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        #elif event.type == SDL_MOUSEMOTION:
        #    team[select].x,team[select].y = event.x,600-event.y
        elif event.type == SDL_KEYDOWN and event.key == SDLK_DOWN:
            if select < maxplayer-1:
                select +=1
            else:
                select = 0
        elif event.type == SDL_KEYDOWN and event.key == SDLK_UP:
            if select > 0:
                select -=1
            else:
                select = maxplayer - 1
        elif event.type == SDL_KEYDOWN and event.key == SDLK_LEFT:
            team[select].state = Boy.LEFT_RUN
        elif event.type == SDL_KEYUP and event.key == SDLK_LEFT and team[select].state == Boy.LEFT_RUN:
            team[select].state = Boy.LEFT_STAND
        elif event.type == SDL_KEYDOWN and event.key == SDLK_RIGHT:
            team[select].state = Boy.RIGHT_RUN
        elif event.type == SDL_KEYUP and event.key == SDLK_RIGHT and team[select].state == Boy.RIGHT_RUN:
            team[select].state = Boy.RIGHT_STAND
def update():
    pass
  
    
def draw():
    global select,frame_time
    current_time = get_time()

    handle_events()
    for boy in team:
        if (boy.name == team[select].name):
            boy.updatehero(frame_time)
        else:
            boy.update(frame_time)
    back.update(frame_time)
    #delay(0.01)
    clear_canvas()
    grass.draw()
    back.draw()
    for boy in team:
        boy.draw()
    font.draw(10,10,str(team[select].name),(0,0,255))
    update_canvas()

    frame_time = get_time() - current_time
    frame_rate = 1.0/frame_time

    current_time += frame_time
class Grass:
    image = None
    def __init__(self):
        if Grass.image == None:
            Grass.image = load_image('grass.png')
    def draw(self):
        self.image.draw(400, 30)
class Boy:
    
    image = None

    

    PIXEL_PER_METER = 10.0/0.3
    RUN_SPEED_KMPH = 20.0
    RUN_SPEED_MPM = RUN_SPEED_KMPH*1000/60.0
    RUN_SPEED_MPS = RUN_SPEED_MPM/60.0
    RUN_SPEED_PPS = RUN_SPEED_MPS * PIXEL_PER_METER

    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0/TIME_PER_ACTION
    FRAMES_PER_ACTION = 8

    
    

    LEFT_RUN,RIGHT_RUN,LEFT_STAND,RIGHT_STAND = 0,1,2,3

    def __init__(self):
        self.x, self.y = random.randint(100,700),90
        self.frame = random.randint(0, 7)
        self.dir = 1
        self.total_frames = 0
        self.run_frames = random.randint(0,100)
        self.stand_frames = 0
        self.state = self.RIGHT_RUN
        if Boy.image == None:
            Boy.image = load_image('animation_sheet.png')
    
    def handle_right_run(self,distance):
        self.x+=distance
        self.run_frames+=1
        if self.x>800:
            self.x = 800
            self.state = self.LEFT_RUN
        if self.run_frames >= 100:
            self.state = self.RIGHT_STAND
            self.stand_frames = 0
    def handle_right_stand(self,distance):
        self.stand_frames+=1
        if self.stand_frames >= 50:
            self.state = self.RIGHT_RUN
            self.run_frames = 0
    def handle_left_run(self,distance):
        self.x-=distance
        self.run_frames+=1
        if self.x<0:
            self.x = 0
            self.state = self.RIGHT_RUN
        if self.run_frames >= 100:
            self.state = self.LEFT_STAND
            self.stand_frames = 0
    def handle_left_stand(self,distance):
        self.stand_frames+=1
        if self.stand_frames >= 50:
            self.state = self.LEFT_RUN
            self.run_frames = 0
            


    handle_state = {
        LEFT_RUN:handle_left_run,
        RIGHT_RUN:handle_right_run,
        LEFT_STAND: handle_left_stand,
        RIGHT_STAND: handle_right_stand
        }
    
    def update(self,frame_time):
        distance = Boy.RUN_SPEED_PPS * frame_time
        self.total_frames += Boy.FRAMES_PER_ACTION * Boy.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % 8
        self.handle_state[self.state](self,distance)
    def updatehero(self,frame_time):
        distance = Boy.RUN_SPEED_PPS * frame_time
        self.total_frames += Boy.FRAMES_PER_ACTION * Boy.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % 8
        if self.state == self.RIGHT_RUN:
            self.x = min(800, self.x + distance)
        elif self.state == self.LEFT_RUN:
            self.x = max(0,self.x-distance)
    def draw(self):
        self.image.clip_draw(self.frame*100, self.state*100, 100, 100, self.x, self.y)
