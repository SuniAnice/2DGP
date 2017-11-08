from pico2d import *
import os
os.chdir('c:\\Users\\Lenovo\\Desktop\\2D')
import random
open_canvas()


class TileBackground:
    PIXEL_PER_METER = (10.0 / 0.3)  # 10pixel30
    SCROLL_SPEED_KMPH = 20.0  # km/hour
    SCROLL_SPEED_MPM = (SCROLL_SPEED_KMPH * 1000.0 / 60.)
    SCROLL_SPEED_MPS = (SCROLL_SPEED_MPM / 60.0)
    SCROLL_SPEED_PPS = (SCROLL_SPEED_MPS * PIXEL_PER_METER)
    def __init__(self,filename,width,height):
        f=open(filename)
        self.map=json.load(f)
        self.layerIndex=0
        self.canvasWidth=width
        self.canvasHeight=height
        self.x=0
        self.y=0
        self.speedX=0
        self.speedY=0
    def draw(self):
        map_width=self.map['width']
        map_height=self.map['height']
        data=self.map['layers'][self.layerIndex]['data']
        tileset=self.map['tilesets'][0]
        tile_width=tileset['tilewidth']
        tile_height=tileset['tileheight']
        margin=tileset['margin']
        spacing=tileset['spacing']
        columns=tileset['columns']
        rows=-(-tileset['tilecount']//columns)#math.cell()
        startx=tile_width//2-self.x%tile_width
        starty=tile_height//2-self.y%tile_height
        endx=self.canvasWidth+tile_width
        endy=self.canvasHeight+tile_height
        desty=starty
        my=int(self.y//tile_height)
        while (desty<endy):
            destx=startx
            mx=int(self.x//tile_width)
            while (destx<endx):
                index=(map_height-my-1)*map_width+mx
                tile=data[index]
                tx=(tile-1)%columns
                ty=rows-(tile-1)//columns-1
                srcx=margin+tx*(tile_width+spacing)
                srcy=self.image.h-margin+ty*(tile_height+spacing)
                self.image.clip.draw(srcx,srcy,tile_width,tile_height,destx,desty)
                destx+=tile_width
                print(x,y,index,tile,srcx,srcy,destx,desty)
            desty+=tile_heght
    def update(self,frametime):
        self.left=(self.left+frame_time*self.speed)%self.image.w
    def handle_event(self,event):
        if event.type==SDL_KEYDOWN:
            if event.key==SDLK_LEFT:
                self.speed-=TileBackground.SCROLL_SPEED_PPS
            elif event.key==SDLK_RIGHT:
                self.speed+=TileBackground.SCROLL_SPEED_PPS
        if event.type==SDL_KEYUP:
            if event.key==SDLK_LEFT:
                self.speed+=TileBackground.SCROLL_SPEED_PPS
            elif event.key==SDLK_RIGHT:
                self.speed-=TileBackground.SCROLL_SPEED_PPS
                                
running=True
class Boy:
    image= None
    
    PIXEL_PER_METER=(10.0/0.3)#10pixel30
    RUN_SPEED_KMPH=20.0#km/hour
    RUN_SPEED_MPM=(RUN_SPEED_KMPH*1000.0/60.)
    RUN_SPEED_MPS=(RUN_SPEED_MPM/60.0)
    RUN_SPEED_PPS=(RUN_SPEED_MPS*PIXEL_PER_METER)
    
    TIMER_PER_ACTION=0.5
    ACTION_PER_TIME=1.0/TIMER_PER_ACTION
    FRAMES_PER_ACTION=8
    
    LEFT_RUN,RIGHT_RUN,LEFT_STAND,RIGHT_STAND=0,1,2,3
    def __init__(self):
        self.x,self.y=random.randint(100,700),90
        self.frame=0
        self.dir=1
        self.run_frames=0
        self.stand_frames=0
        self.total_frames=0
        self.state=random.randint(2,3)
        if Boy.image==None:
            Boy.image=load_image('animation_sheet.png')
        if  Boy.eat_sound==None:
            Boy.eat_sound==load_wav('pickup.wav')
            Boy.eat_sound.set_volume(32)
    def eat(self,ball):
        self.eat_sound.play()
    def handle_left_run(self,distance):
        self.x-=(distance)
        self.run_frames+=1
        if self.x<0:
            self.x=0
    def handle_left_stand(self,distance):
        self.stand_frames+=1
    def handle_right_run(self,distance):
        self.x+=(distance)
        self.run_frames+=1
        if self.x>800:
            self.x=800
    def handle_right_stand(self,distance):
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
    def update(self,frame_time):
        distance=Boy.RUN_SPEED_PPS*frame_time
        self.total_frames+=Boy.FRAMES_PER_ACTION*Boy.ACTION_PER_TIME*frame_time
        self.frame=int(self.total_frames)%8
        self.handle_state[self.state](self,distance)
        if self.state==self.RIGHT_RUN:
            self.x=min(800,self.x+5)
        elif self.state==self.LEFT_RUN:
            self.x=max(0,self.x-5)

    def draw(self):
        self.image.clip_draw(self.frame*100,self.state*100,100,100,self.x,self.y)

    def get_bb(self):
        return self.x-50,self.y-50,self.x+50,self.y+50
    def draw_bb(self):
        draw_rectangle(*self.get_bb())
class Grass:
    def __init__(self):
        self.image=load_image('grass.png')
        self.bgm=load_music('football.mp3')
        self.bgm.set_volume(64)
        self.bgm.repeat_play()
        self.x,self.y=200,15
    def draw(self):
        self.image.draw(400,30)
    def get_bb(self):
        return self.x-200,self.y-15,self.x+200,self.y+15
    def draw_bb(self):
        draw_rectangle(*self.get_bb())

class Ball :
    image=None;
    def __init__(self):
        self.x,self.y,=random.randint(200,790),60
        if Ball.image==None:
            Ball.image=load_image('ball21x21.png')
    def update(self,frame_time):
        pass
    def draw(self):
        self.image.draw(self.x,self.y)
    def get_bb(self):
        return self.x-10,self.y-10,self.x+10,self.y+10
    def draw_bb(self):
        draw_rectangle(*self.get_bb())

class BigBall(Ball):
    image=None;
    def __init__(self):
        self.x,self.y=random.randint(100,700),500
        self.fall_speed=random.randint(50,120)
        if BigBall.image==None:
            BigBall.image=load_image('ball41x41.png')
    def update(self,frame_time):
        self.y-=frame_time*self.fall_speed
    def get_bb(self):
        return self.x-20,self.y-20,self.x+20,self.y+20
    def stop(self):
        self.fall_speed=0
    def draw_bb(self):
        draw_rectangle(*self.get_bb())

class Background:
    image=None
    PIXEL_PER_METER = (10.0 / 0.3)  # 10pixel30
    SCROLL_SPEED_KMPH = 20.0  # km/hour
    SCROLL_SPEED_MPM = (SCROLL_SPEED_KMPH * 1000.0 / 60.)
    SCROLL_SPEED_MPS = (SCROLL_SPEED_MPM / 60.0)
    SCROLL_SPEED_PPS = (SCROLL_SPEED_MPS * PIXEL_PER_METER)
    def __init__(self,w,h):
        self.left=0
        self.screen_width=w
        self.screen_height=h
        self.speed=0
        if Background.image==None:
            Background.image=load_image('background.png')
    def draw(self):
        x=int(self.left)
        w=min(self.image.w-x,self.screen_width)
        self.image.clip_draw_to_origin(x,0,w,self.screen_height,0,0)
        self.image.clip_draw_to_origin(0,0,self.screen_width-w,self.screen_height,w,0)

    def update(self,frame_time):
        self.left=(self.left+frame_time*self.speed)%self.image.w
    def handle_event(self,event):
        if event.type==SDL_KEYDOWN:
            if event.key==SDLK_LEFT:
                self.speed-=Background.SCROLL_SPEED_PPS
            elif event.key==SDLK_RIGHT:
                self.speed+=Background.SCROLL_SPEED_PPS
        if event.type==SDL_KEYUP:
            if event.key==SDLK_LEFT:
                self.speed+=Background.SCROLL_SPEED_PPS
            elif event.key==SDLK_RIGHT:
                self.speed-=Background.SCROLL_SPEED_PPS

def enter():
    global team,grass,z,s,a,frame_time,balls,big_balls,background,TILE
    team=[Boy() for i in range(11)]
    TILE=TileBackground('map.json',250,250)
    grass=Grass()
    z=0
    s=str(z)
    big_balls=[BigBall()for i in range(10)]
    a=load_font('Consola.ttf',20)
    frame_time=0.1
    balls=[Ball()for i in range(10)]
    balls=big_balls+balls
    background=Background(960,700)

def exit():
    global boy,grass,team,balls
    del(team)
    del(grass)
    del(balls)
    
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
           if z>11:
               z=11
           s=str(z)
       elif event.key==SDLK_DOWN:
           z-=1
           if z<0:
               z=0
           s=str(z)
       elif event.key==SDLK_ESCAPE:
            running=False
       else :
            team[z].handle_event(event)
            background.handle_event(event)
  elif event.type==SDL_KEYUP:
      team[z].handle_event(event)
      background.handle_event(event)
  elif event.type==SDL_MOUSEMOTION: 
       team[z].x,team[z].y=event.x,600-event.y

def update():
    global frame_time
    for boy in team:
        boy.update(frame_time)
    for ball in balls:
        ball.update(frame_time)
    for ball in balls:
        if collide(boy,ball):
            balls.remove(ball)
            boy.eat(ball)
    for ball in big_balls:
        if collide(grass,ball):
            ball.stop()
    background.update(frame_time)

def collide(a,b):
    left_a,bottom_a,right_a,top_a=a.get_bb()
    left_b,bottom_b,right_b,top_b=b.get_bb()

    if left_a> right_b: return False
    if right_a< left_b:return False
    if top_a<bottom_b:return False
    if bottom_a>top_b:return False

    return True


def draw():
    global frame_time
    current_time=get_time()
    clear_canvas()
    grass.draw()
    background.draw()
    for boy in team:
        boy.draw()
    for ball in balls:
        ball.draw()
    
    grass.draw_bb()
    boy.draw_bb()
    for ball in balls:
        ball.draw_bb()
    a.draw(100,50,s,(0,255,0))
    TILE.draw()
    update_canvas()

    frame_time=get_time()-current_time
    frame_rate=1.0/frame_time
    print("Frame Rate: %f fps, Frame Time: %f sec, "%(frame_rate,frame_time))
    
    current_time+=frame_time


    
enter()
while (running):
   
    draw()
    update()
    handle_events()

