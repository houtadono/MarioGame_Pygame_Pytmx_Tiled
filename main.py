import pygame
import pytmx

from mario import *
from spritebase import *
from sprites_group import *
from coinbox import *
from brick import *
from turtlee import *
from flower import *
from invisible import *
from config import *

class MarioGame:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Mario Game')
        self.screen = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT),pygame.RESIZABLE)
        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('SF Mono',23)
        self.time_step = 0
        self.running = True
        self.tmx_data = pytmx.load_pygame("./Tiled/untitled.tmx")

    def init(self):
        # load back-mid-foreGround

        self.tiles_group = Sprites_group()

        for layer in self.tmx_data.layers:
            if hasattr(layer,'data'):
                for x,y,surf in layer.tiles():
                    pos = (x*TILE_WIDTH, y*TILE_HEIGHT)
                    Tile(pos,surf,self.tiles_group)
        # load Triggers
        # player
        player = self.tmx_data.get_object_by_name('Player')
        self.mario = Mario(player.properties['size'], (player.x,player.y))
        

        self.triggers_group = Sprites_group()
        self.checkpoints = {}

        for cell in self.tmx_data.get_layer_by_name('Triggers'):
            a = 0
            pos = cell.x,cell.y
            if 'coinbox' in cell.properties:
                a = Coinbox( cell.properties['count'], pos, cell.properties['coinbox'], self.triggers_group) 

            if 'brick' in cell.properties:
                a = Brick(cell.properties['index'], pos, cell.properties['brick'], self.triggers_group)

            if cell.name == "Turtle":
                a = Turtlee(cell.properties['live'], pos, self.triggers_group)

            if  cell.name == "Flower":
                a = Flower(cell.properties['color'], pos, self.triggers_group)

            if 'blocker' in cell.properties :
                if a != 0:
                    a.set_blocker(cell.properties['blocker'])
                else:
                    rect_invisible = pygame.Rect(cell.x,cell.y, cell.width,cell.height)
                    Invisible(cell.properties['blocker'], rect_invisible, self.triggers_group) # this is Floor / Wall/ River / Pipe,........ (rectangle) no draw, update...

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.time_step += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            self.handle(event)
            self.update()
            self.draw()
                  
    def update(self):
        self.mario.update(self)
        self.triggers_group.update(self) 

    def draw(self):
        self.screen.fill((95, 183, 229))
        set_camera(self.mario)

        self.tiles_group.draw(self.screen, OFFSET_CAMERA)
        self.triggers_group.draw(self.screen, OFFSET_CAMERA) 
        self.mario.draw(self.screen, OFFSET_CAMERA)

        pygame.display.update()   

    def handle(self, event):
        self.mario.handle(event)

    def restart(self):
        self.init()

    # def 

    # def intro_screen(self):

if __name__ == '__main__':
    a = MarioGame()
    a.init()
    a.run()