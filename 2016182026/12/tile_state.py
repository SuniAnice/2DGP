from pico2d import *
import json
import random
class TileBackground:
    SCROLL_SPEED_PPS = 300
    def __init__(self,filename,width,height):
        f=open(filename)
        self.map=json.load(f)
        self.layerIndex=0
        self.canvas_width=width
        self.canvas_height=height
        self.window_left=0
        self.window_bottom=0
        self.speedX=0
        self.speedY=0
        tileset=self.map['tilesets'][0]
        image_filename=tileset['image']
        self.image=load_image('tmw_desert_spacing.png')
        self.w=tileset['tilewidth']*self.map['width']
        self.h=tileset['tileheight']*self.map['height']
        
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
        startx=tile_width//2-self.window_left%tile_width
        starty=tile_height//2-self.window_bottom%tile_height
        endx=self.canvas_width+tile_width//2
        endy=self.canvas_height+tile_height//2
        desty=starty
        my=int(self.window_bottom//tile_height)
        while (desty<endy):
            destx=startx
            mx=int(self.window_left//tile_width)
            while (destx<endx):
                index=(map_height-my-1)*map_width+mx
                tile=data[index]
                tx=(tile-1)%columns
                ty=rows-(tile-1)//columns-1
                srcx=margin+tx*(tile_width+spacing)
                srcy=margin+ty*(tile_height+spacing)
                self.image.clip_draw(srcx,srcy,tile_width,tile_height,destx,desty)
                destx+=tile_width
                mx+=1
            desty+=tile_height
            my+=1

    def set_center_object(self,boy):
        self.center_object=boy

        
    def update(self,frame_time):
        self.window_left=clamp(0,int(self.center_object.x)-self.canvas_width//2,
                               self.w-self.canvas_width)
        self.window_bottom=clamp(0,int(self.center_object.y)-self.canvas_height//2,
                                 self.h-self.canvas_height)

            
    def handle_event(self,event):
        if event.type==SDL_KEYDOWN:
            if event.key==SDLK_LEFT:
                self.speedX-=TileBackground.SCROLL_SPEED_PPS
            elif event.key==SDLK_RIGHT:
                self.speedX+=TileBackground.SCROLL_SPEED_PPS
            elif event.key==SDLK_UP:
                self.speedY+=TileBackground.SCROLL_SPEED_PPS
            elif event.key==SDLK_DOWN:
                self.speedY-=TileBackground.SCROLL_SPEED_PPS
        if event.type==SDL_KEYUP:
            if event.key==SDLK_LEFT:
                self.speedX=0
            elif event.key==SDLK_RIGHT:
                self.speedX=0
            elif event.key==SDLK_UP:
                self.speedY=0
            elif event.key==SDLK_DOWN:
                self.speedY=0
                                

