from pico2d import *
import game_framework
import random
import title_state
import json_player
def enter():
    global team, grass,select,font
    open_canvas()
    Boy.image = None
    Grass.image = None
    json_player.create_team()
    select = 0
    grass = Grass()
    font = load_font('Consola.ttf',25)
def exit():
    global team, grass,font
    del(team)
    del(grass)
    del(font)
    close_canvas()
def handle_events():
    global select
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_state(title_state)
        elif event.type == SDL_MOUSEMOTION:
            team[select].x,team[select].y = event.x,600-event.y
        elif event.type == SDL_KEYDOWN and event.key == SDLK_DOWN:
            if select < 1000:
                select +=1
        elif event.type == SDL_KEYDOWN and event.key == SDLK_UP:
            if select > 0:
                select -=1
def update():
    for boy in team:
        boy.update()
    delay(0.05)
def draw():
    global select
    clear_canvas()
    grass.draw()
    for boy in team:
        boy.draw()
    font.draw(10,10,str(select),(0,0,255))
    update_canvas()
class Grass:
    image = None
    def __init__(self):
        if Grass.image == None:
            Grass.image = load_image('grass.png')
    def draw(self):
        self.image.draw(400, 30)
class Boy:
    image = None

    LEFT_RUN,RIGHT_RUN,LEFT_STAND,RIGHT_STAND = 0,1,2,3

    
    
    def __init__(self):
        self.x, self.y = random.randint(100,700),90
        self.frame = random.randint(0, 7)
        self.dir = 1
        self.run_frames = random.randint(0,100)
        self.stand_frames = 0
        self.state = self.RIGHT_RUN
        if Boy.image == None:
            Boy.image = load_image('animation_sheet.png')
    def handle_right_run(self):
        self.x+=5
        self.run_frames+=1
        if self.x>800:
            self.x = 800
            self.state = self.LEFT_RUN
        if self.run_frames == 100:
            self.state = self.RIGHT_STAND
            self.stand_frames = 0
    def handle_right_stand(self):
        self.stand_frames+=1
        if self.stand_frames == 50:
            self.state = self.RIGHT_RUN
            self.run_frames = 0
    def handle_left_run(self):
        self.x-=5
        self.run_frames+=1
        if self.x<0:
            self.x = 0
            self.state = self.RIGHT_RUN
        if self.run_frames == 100:
            self.state = self.LEFT_STAND
            self.stand_frames = 0
    def handle_left_stand(self):
        self.stand_frames+=1
        if self.stand_frames == 50:
            self.state = self.LEFT_RUN
            self.run_frames = 0
    handle_state = {
        LEFT_RUN:handle_left_run,
        RIGHT_RUN:handle_right_run,
        LEFT_STAND: handle_left_stand,
        RIGHT_STAND: handle_right_stand
        }
    def update(self):
        self.frame = (self.frame + 1) % 8
        self.handle_state[self.state](self)
    def draw(self):
        self.image.clip_draw(self.frame*100, self.state*100, 100, 100, self.x, self.y)
