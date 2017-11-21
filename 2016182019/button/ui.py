from pico2d import *
import game_framework

ui_objects = []

def handle_event(event):
    for obj in ui_objects:
        obj.handle_event(event)

def draw():
    for obj in ui_objects:
        obj.draw()

class Button:
    font = None
    def __init__(self,imageFilename,hoverFilename,x=0,y=0):
        self.image = load_image(imageFilename)
        if hoverFilename == None:
            self.hoverimage = None
        else:
            self.hoverimage = load_image(hoverFilename)
        self.x,self.y = x,y
        self.hover = False
        self.add()
        if Button.font == None:
            Button.font = load_font('ConsolaMalgun.ttf')

    def draw(self):
        image = self.hoverimage if self.hover else self.image
        image.draw(self.x,self.y)
        if self.text !="":
            w = len(self.text) * 10
            h = 30
            x = self.x - w/2
            y = self.y - h/2
            self.font.draw(x,y,self.text)


    def ptInRect(self,x,y):
        if (x>=self.x-self.image.w/2) and (x<=self.x+self.image.w/2) and (y>=self.y-self.image.h/2) and (y<=self.y+self.image.h/2):
            return True
        else:
            return False

    def add(self):
        ui_objects.append(self)

    def handle_event(self,event):
        if event.type == SDL_MOUSEMOTION:
            if self.hoverimage !=None:
                self.hover = self.ptInRect(event.x, event.y)
        if event.type == SDL_MOUSEBUTTONDOWN:
            if self.ptInRect(event.x,event.y):
                self.onClick()

    def onOver(self):
        print(self)

    def onClick(self):
        pass