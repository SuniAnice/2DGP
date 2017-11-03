from pico2d import *
import os
os.chdir('c:\\Users\\Lenovo\\Desktop\\2D')
import title_state
import game_framework
import random
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

def enter():
    global team,grass,z,s,a,frame_time,balls,big_balls
    team=[Boy() for i in range(11)]
    grass=Grass()
    z=0
    s=str(z)
    big_balls=[BigBall()for i in range(10)]
    a=load_font('Consola.ttf',20)
    frame_time=0.1
    balls=[Ball()for i in range(10)]
    balls=big_balls+balls

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
            game_framework.change_state(title_state)
       else :
            team[z].handle_event(event)
  elif event.type==SDL_KEYUP:
      team[z].handle_event(event)
  elif event.type==SDL_MOUSEMOTION: 
       team[z].x,team[z].y=event.x,600-event.y

def update():
    global frame_time
    for boy in team:
        boy.update(frame_time)
    delay(0.07)
    for ball in balls:
        ball.update(frame_time)
    for ball in balls:
        if collide(boy,ball):
            balls.remove(ball)
    for ball in big_balls:
        if collide(grass,ball):
            ball.stop()

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
    for boy in team:
        boy.draw()
    for ball in balls:
        ball.draw()

    grass.draw_bb()
    boy.draw_bb()
    for ball in balls:
        ball.draw_bb()
    a.draw(100,50,s,(0,255,0))
    update_canvas()

    frame_time=get_time()-current_time
    frame_rate=1.0/frame_time
    print("Frame Rate: %f fps, Frame Time: %f sec, "%(frame_rate,frame_time))
    
    current_time+=frame_time

