import pygame
import spritebase
import config

class Turtlee(spritebase.Spritebase):
    FRAME_WIDTH = 20
    FRAME_HEIGHT = 20 
    PADDING = 0

    imgs = ["red_turtlee.png","red_turtlee_shell.png"]
    ANIMATIONS = [[0,1],[0,1,2]]
    ANIMATION_INTERVAL = 5
    MAX_VX = 1 
    speed = 1


    state = "normal"
    h_state = "running"

    def __init__(self, live,pos, group):
        self.check_mario_kick_shell_running = False
        self.live = live 
        self.img_file = self.imgs[0]
        self.FRAMES = self.ANIMATIONS[0]
        self.v_state = 'jumping'
        super(Turtlee,self).__init__(self.frame_index, pos, True, group)
    
    def change_normal_to_shell(self):
        self.FRAME_HEIGHT = 14
        self.MAX_VX = 3
        self.img_file = self.imgs[1]
        self.FRAMES = self.ANIMATIONS[1]
        self.frame_index = self.FRAMES[1]

    def shell_running(self,direct,mario_rect):
        self.rect_after_kick = self.rect.copy()
        self.h_state = "running"
        if direct == 'r':
            self.rect_after_kick.left = mario_rect.left + mario_rect.width
            # self.vx += mario_rect.width
            self.h_facing = 'right'
        else:
            self.rect_after_kick.left = mario_rect.left - mario_rect.width
            self.h_facing = 'left'
            # self.vx -= mario_rect.width 

    def get_hit(self):
        if self.state == 'normal':
            self.state = 'shell'
            self.change_normal_to_shell()
        self.live -= 1
        self.h_state = 'standing'
        if self.live == 0:
            self.blocker = ''

    
    def update(self, game):
        if self.live == 0 and self.h_state != 'out':
            self.vy = -4
            self.h_state = 'out'
            self.set_sprite(1)

        if self.h_facing == "right":
            self.vx += self.speed
        else: 
            self.vx -= self.speed

        if self.h_state == 'standing':
            self.vx = 0  
        last = self.rect.copy()

        if hasattr(self, 'rect_after_kick') and self.rect_after_kick != None:
            new = self.accept_gravity(self.rect_after_kick)
            self.rect_after_kick = None
        else:
            new = self.accept_gravity(last)

        self.rect = new 

        if self.h_state == 'out':
            return

        for sprite in game.triggers_group.sprites():
            if type(sprite).__name__ == "Turtlee": continue
            if hasattr(sprite,'blocker') and sprite.rect.colliderect(new):
                value_blocker = sprite.blocker
                test = ''
                if 'l' in value_blocker and last.right <= sprite.rect.left and new.right > sprite.rect.left:
                    new.right = sprite.rect.left
                    self.vx = 0
                    self.h_facing = 'left'
                    test+='l'

                if 'r' in value_blocker and last.left >= sprite.rect.right and new.left < sprite.rect.right:
                    new.left = sprite.rect.right
                    self.vx = 0
                    self.h_facing = 'right'
                    test+='r'

                if 't' in value_blocker and last.bottom <= sprite.rect.top and new.bottom > sprite.rect.top:
                    new.bottom = sprite.rect.top
                    self.vy = 0
                    self.v_state = 'resting'
                    test+='t'
                    
        
                if 'b' in value_blocker and last.top >= sprite.rect.bottom and new.top < sprite.rect.bottom:
                    new.top = sprite.rect.bottom
                    self.vy = 0
                    test+='b'

                if test == '' and self.v_state == 'resting':
                    self.live = 0
                    self.blocker = ''
                

        self.rect = new 
        if self.h_state == 'standing':
            self.set_sprite(1)
            self.vx = 0             
        else:
            super(Turtlee,self).update(game)
    