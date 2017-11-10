import random

from pico2d import *

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
    def update(self,frame_time):
        self.window_left = clamp(0,int(self.center_object.x) - self.canvasWidth//2,
                                 self.w-self.canvasWidth)
        self.window_bottom = clamp(0,
                                   int(self.center_object.y)-self.canvasHeight//2,
                                  self.h - self.canvasHeight)
    def handle_event(self,event):
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

        startx = tile_width // 2-self.window_left
        starty = tile_height // 2-self.window_bottom

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


