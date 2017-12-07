from pico2d import *
import game_framework
import json
import pickle

# False일시 json, True일시 pickle
usepickle = True

name = 'score_state'

scores = []

filename = ""

if (usepickle == True):
    filename = "score.pickle"
else:
    filename = "score.json"


class Entry:
    def __init__(self,score,time):
        self.score = score
        self.time = time



def add(score):
    global scores
    #scores.append(score)
    if len(scores) == 0:
        scores.append(score)
    else:
        for i in range(len(scores)):
            if scores[i].score < score.score:
                scores.insert(i,score)
                break
            if i == (len(scores)-1):
                scores.append(score)
                break


    print("Now score has " + str(len(scores)) + " Entries.")
    savescore()

def loadscore():
    global scores
    scores = []
    if (usepickle):
        f = open(filename, 'rb')
        scores = pickle.load(f)
        f.close()
    else:
        f = open(filename, 'r')
        scores = json.load(f)
        f.close()
def savescore():
    global scores
    if (usepickle):
        f = open(filename,'wb')
        pickle.dump(scores,f)
        f.close()
    else:
        f = open(filename, 'w')
        json.dump(scores, f)
        f.close()

def enter():
    global font
    open_canvas()
    loadscore()
    font = load_font('Consola.ttf')


def exit():
    close_canvas()
def handle_events():
    global scores
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_x:
            if (usepickle):
                scores = []
                f = open(filename, 'wb')
                pickle.dump(scores,f)
                f.close()
            else:
                scores = []
                f = open(filename, 'w')
                json.dump(scores, f)
                f.close()
        elif event.type == SDL_KEYDOWN:
            game_framework.pop_state()
def update():
    pass
def draw():
    clear_canvas()
    for i in range(min(len(scores),10)):
        font.draw(200,550-30*i,str({scores[i].score : scores[i].time}))
    update_canvas()

loadscore()
