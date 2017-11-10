from pico2d import *
import game_framework
import random
import time
import json
import json_player
'''
    def update(self):
        global frame_time,tile_width
        if ((self.x + self.speedx * frame_time) < 0):
            self.x = 0
        elif (self.x + self.speedx * frame_time > 2000):
            self.x = 2000
        else:
            self.x+=self.speedx * frame_time
        if ((self.y + self.speedy * frame_time) < 0):
            self.y = 0
        elif (self.y + self.speedy * frame_time > 2000):
            self.y = 2000
        else:
            self.y+=self.speedy * frame_time
'''
name = 'Main_state'

canvasWidth = 800
canvasHeight = 600
SCROLL_SPEED_PPS = 300
class TileBackground:
    
    def __init__(self,fliename,width,height):
        f = open('map.json')
        self.map = json.load(f)
        tileset = self.map['tilesets'][0]
        self.x = 0
        self.y = 0
        self.layerindex = 0
        self.speedx = 0
        self.speedy = 0
        self.canvasWidth = width
        self.canvasHeight = height
        self.w = tileset['tilewidth'] * self.map['width']
        self.h = tileset['tileheight'] * self.map['height']
        image_filename = tileset['image']
        self.image = load_image('tmw_desert_spacing.png')

    def set_center_object(self, boy):
        self.center_object = boy
    def update(self):
        self.window_left = clamp(0,int(self.center_object.x) - self.canvasWidth//2,
                                 self.w-self.canvasWidth)
        self.window_bottom = clamp(0,
                                   int(self.center_object.y)-self.canvasHeight//2,
                                  self.h - self.canvasHeight)
    def handle_events(self,event):
        if event.type == SDL_KEYDOWN and event.key == SDLK_LEFT:
            self.speedx = - SCROLL_SPEED_PPS
        elif event.type == SDL_KEYDOWN and event.key == SDLK_RIGHT:
            self.speedx =SCROLL_SPEED_PPS
        elif event.type == SDL_KEYDOWN and event.key == SDLK_UP:
            self.speedy =SCROLL_SPEED_PPS
        elif event.type == SDL_KEYDOWN and event.key == SDLK_DOWN:
            self.speedy =-SCROLL_SPEED_PPS

        if event.type == SDL_KEYUP and event.key == SDLK_LEFT:
            self.speedx = 0
        elif event.type == SDL_KEYUP and event.key == SDLK_RIGHT:
            self.speedx =0
        elif event.type == SDL_KEYUP and event.key == SDLK_UP:
            self.speedy =0
        elif event.type == SDL_KEYUP and event.key == SDLK_DOWN:
            self.speedy =0
        
    def draw(self):
        global tile_width
        map_width = self.map['width']
        map_height = self.map['height']
        data = self.map['layers'][0]['data']
        tileset = self.map['tilesets'][0]
        tile_width = tileset['tilewidth']
        tile_height = tileset['tileheight']
        margin = tileset['margin']
        spacing = tileset['spacing']
        columns = tileset['columns']
        rows = - (-tileset['tilecount'] // columns)

        startx = tile_width // 2 - self.x % tile_width
        starty = tile_height // 2 - self.y % tile_height

        endx = self.canvasWidth + tile_width // 2
        endy = self.canvasHeight + tile_height // 2
        
        desty = starty
        my = int(self.y // tile_height)
        while(desty<endy):
            destx = startx
            mx = int(self.x // tile_width)
            while(destx<endx):
                index = (map_height-my-1) * map_width + mx
                tile = data[index]
                tx = (tile-1) % columns
                ty = rows - (tile - 1) // columns - 1
                srcx = margin + tx * (tile_width + spacing)
                srcy = margin + ty * (tile_height + spacing)
                self.image.clip_draw(srcx,srcy,tile_width,tile_height,destx,desty)
                destx+=tile_width
                mx+=1
                
            desty +=tile_height
            my+=1
def enter():
    global team, grass,select,font,frame_time,maxplayer,back
    open_canvas(canvasWidth,canvasHeight)
    Boy.image = None
    Grass.image = None
    frame_time = 0.01
    team,maxplayer = json_player.create_team()
    select = 0
    grass = Grass()
    back = TileBackground('map.json',canvasWidth,canvasHeight)
    font = load_font('Consola.ttf',25)
def exit():
    global team, grass,font,back
    del(grass)
    del(font)
    del(team)
    del(back)
    close_canvas()
def handle_events():
    global select,Boy,maxplayer,back
    events = get_events()
    for event in events:
        #back.handle_events(event)
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
    back.set_center_object(team[select])
    back.update()
    delay(0.01)
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
    RUN_SPEED_KMPH = 40.0
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
