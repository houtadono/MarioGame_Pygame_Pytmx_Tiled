import pygame

import config
import spritebase
import os

class Brick(spritebase.Spritebase):

    img_file = "map.png"
    broken_file = "part.png"
    PART_GRAVITY = 0.2
    FRAME_WIDTH = 20
    FRAME_HEIGHT = 14
    PADDING = 0
    TILE = [3, 4]

    def __init__(self, index, pos, hidden, group):
        self.check_broken = False
        super(Brick,self).__init__(self.TILE[0], pos, hidden, group)

    def get_hit(self,mario_size):
        if mario_size == 'small':
            self.jump(2)
            self.old_bottom = self.rect.bottom
            return
        if self.check_broken == True: 
            return
        self.set_blocker('')
        self.check_broken = True
        self.brokens = 4 * [ None]
        self.brokens_vx = [-2, -2, 2, 2]
        self.brokens_vy = [-6, -2, -2, -6]
        location = (self.rect.centerx - 5/2, self.rect.centery - 5/2) 
        broken_img = pygame.image.load(os.path.join(config.image_path,self.broken_file))

        for i in range(4):
            self.brokens[i] = pygame.sprite.Sprite()
            self.brokens[i].image = broken_img
            self.brokens[i].rect = self.brokens[i].image.get_rect()
            self.brokens[i].rect.centerx = self.rect.centerx
            self.brokens[i].rect.top = self.rect.top


    def update(self, game):
        if self.check_broken == False : return 
        for i in range(len(self.brokens)):
            if self.brokens[i] != None:
                self.brokens[i].rect.x += self.brokens_vx[i]
                self.brokens[i].rect.y += self.brokens_vy[i]
                self.brokens[i].rect = self.accept_gravity(self.brokens[i].rect)
                if self.brokens[i].rect.top > config.WIN_HEIGHT:
                    self.brokens[i].kill()  
                    self.brokens[i] = None
        if self.brokens.count(None) == 4:
            self.kill()
                

    def draw(self, screen, offset):
        if self.v_state == 'jumping':
            new = self.accept_gravity(self.rect)
            if new.bottom > self.old_bottom:
                new.bottom = self.old_bottom
                self.v_state = 'resting'
            self.rect = new 
        if not self.check_broken:
            return super().draw(screen, offset)
        for i in range(len(self.brokens)):
            if self.brokens[i] != None:
                screen.blit(self.brokens[i].image, self.brokens[i].rect.topleft - offset)
        
        