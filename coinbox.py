import pygame
import spritebase
import config

class Coinbox(spritebase.Spritebase):
    img_file = "map.png"
    FRAME_WIDTH = 20
    FRAME_HEIGHT = 14
    PADDING = 0

    ANIMATIONS = [0,1]
    ANIMATION_INTERVAL = 10

    def __init__(self, count, pos, hidden, group):
        self.FRAMES = self.ANIMATIONS
        self.frame_index = self.FRAMES[0]
        self.count = count
        super(Coinbox,self).__init__(self.frame_index, pos, hidden, group)

    def get_hit(self):
        if self.count == 0:
            pass
        else: # hộp rung lên và rơi item
            # rung (cho jump up and chịu lực hấp dẫn trở về vị trí cũ)
            self.jump(2)
            self.old_bottom = self.rect.bottom
            self.count -= 1
            config.play_sound(config.coinbox_sound)

    def update(self, game):
        if self.v_state == 'jumping':
            new = self.accept_gravity(self.rect)
            if new.bottom > self.old_bottom:
                new.bottom = self.old_bottom
                self.v_state = 'resting'
            self.rect = new 
            

        if self.count > 0:
            super(Coinbox,self).update(game)
        else :
            self.set_sprite(2)
    