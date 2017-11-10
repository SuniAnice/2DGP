from pico2d import *
import game_framework
import random
import main_state

name = 'main_state'

def enter():
    global team, grass,balls
    open_canvas()
    team = [Boy() for i in range(1)]
    balls = [Ball() for i in range(10)]
    grass = Grass()
def exit():
    global team, grass,balls
    del(team)
    del(grass)
    del(balls)
    close_canvas()
def handle_events():
    global select
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_MOUSEMOTION:
            team[0].x,team[0].y = event.x,600-event.y
def update():
    for boy in team:
        boy.update()
    for ball in balls:
        if collide(boy,ball):
            balls.remove(ball)
            Boy.eat_sound.play()
    delay(0.05)
def draw():
    clear_canvas()
    grass.draw()
    for Ball in balls:
        Ball.draw()
    for boy in team:
        boy.draw()
    update_canvas()
def collide(a,b):
    left_a,bot_a,right_a,top_a = a.get_bb()
    left_b,bot_b,right_b,top_b = b.get_bb()

    if left_a>right_b:return False
    if right_a<left_b:return False
    if top_a<bot_b:return False
    if bot_a>top_b:return False

    return True
class Grass:
    def __init__(self):
        self.image = load_image('grass.png')
        self.bgm = load_music('football.mp3')
        self.bgm.set_volume(64)
        self.bgm.repeat_play()

    def draw(self):
        self.image.draw(400, 30)
class Boy:
    eat_sound = None
    def __init__(self):
        self.x, self.y = random.randint(100,700),90
        self.frame = random.randint(0, 7)
        self.image = load_image('run_animation.png')
        if Boy.eat_sound == None:
            Boy.eat_sound = load_wav('pickup.wav')
            Boy.eat_sound.set_volume(32)
    def update(self):
        self.frame = (self.frame + 1) % 8
    def draw(self):
        self.image.clip_draw(self.frame*100, 0, 100, 100, self.x, self.y)
    def get_bb(self):
        return self.x-20,self.y-50,self.x+20,self.y+50

class Ball:
    image = None
    def __init__(self):
        self.x,self.y = random.randint(200,790),random.randint(100,590)
        if Ball.image == None:
            Ball.image = load_image('ball21x21.png')
    def draw(self):
        self.image.draw(self.x,self.y)
    def get_bb(self):
        return self.x-10,self.y-10,self.x+10,self.y+10

if __name__ == '__main__':
    game_framework.run(main_state)
