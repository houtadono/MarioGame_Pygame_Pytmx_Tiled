import pygame
import spritebase
import config

class Flower(spritebase.Spritebase):
    FRAME_WIDTH = 24
    FRAME_HEIGHT = 17 
    PADDING = 1

    img_file = 'flower.png'
    v_facing = "down"
    V_FACINGS = ["down","up"]
    ANIMATION_INTERVAL = 80

    def __init__(self, color, pos, group):
        self.color = color
        if color == 'green':
            self.FRAMES = [2,3]
        else:
            self.FRAMES = [0,1]

        super(Flower,self).__init__(self.FRAMES[0], pos, True, group)
        self.rect.top  += (config.TILE_HEIGHT - self.FRAME_HEIGHT)
        self.rect.left += (config.TILE_WIDTH - self.FRAME_WIDTH//2)

    def update(self, game):
        if game.time_step % self.ANIMATION_INTERVAL == 0:
            super().update(game)
            self.v_facing = self.V_FACINGS[self.frame_index]

    