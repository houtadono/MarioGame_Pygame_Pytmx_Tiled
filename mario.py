import math
import pygame
import spritebase
from config import *

class Mario(spritebase.Spritebase):

    sprite_imgs = {
        "small" : "small_mario.png",
        "medium": "medium_mario.png",
        "dying" : "medium_death_mario.png"
    }

    cell_frames = {
        "small":  [ (20,19), (20,19), (20,19), (20,19)],
        "medium": [ (19,26), (19,26), (20,26), (20,27)],
        "dying":  [ (24,24)]
    }

    # animation
    STAND = 0
    RUNNING = [0,1]
    JUMP = 2
    ANIMATION_INTERVAL = 5

    def __init__(self, size, pos):
        self.grow_up(size)
        self.start_location = pos
        self.state = 'normal'
        self.live = 100
        self.FRAMES = self.RUNNING
        super(Mario,self).__init__(self.STAND, pos, True)
        

    def grow_up(self, size,up_top=12):
        if self.rect: 
            old_bot = self.rect.bottom
        else:
            old_bot = -1
        self.size = size
        self.img_file = self.sprite_imgs[size]
        self.frame_sizes = self.cell_frames[size]
        if size == "medium":
            self.opacity = 128
            if self.rect:
                self.rect.top -= 5
        else :
            self.opacity = 255

    def handle(self,event): # khi gõ phím và chỉ chuyển trạng thái
        if self.state == 'dying':
            return
        if event.type == pygame.KEYDOWN: # khi nhấn phím
            if event.key == pygame.K_UP:
                if self.v_state == "resting": # nếu có thể nhảy thì nhảy:)
                    self.jump(9)
            elif event.key == pygame.K_DOWN: # cúi đầu 
                pass
            elif event.key == pygame.K_LEFT:
                self.move_left()
            elif event.key == pygame.K_RIGHT:
                self.move_right()

        elif event.type == pygame.KEYUP: # khi nhả phím
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                self.h_state = 'standing'
                self.vx = 0
            elif event.key == pygame.K_DOWN:
                    self.v_state = "resting"
    
    def move_left(self):
        self.vx = -2.5
        self.h_state = 'running'
        self.h_facing = "left"

    def move_right(self):
        self.vx = 2.5
        self.h_state = "running"
        self.h_facing = "right"

    def set_position(self,x,y):
        self.rect.x = x
        self.rect.y = y

    def reborn(self,game):
        self.grow_up('small')
        self.rect.topleft = self.start_location
        self.state = 'normal'
        self.h_state = 'standing'

    def back_to_normal(self):
        self.state = 'normal'

    def become_invicible(self):
        self.state = 'invicible'
        self.time_invi = 100

    def get_hit(self):
        if self.size != 'small':
            self.grow_up('small')
            self.become_invicible()
        elif self.state != 'invicible':
            self.go_dying()


    def go_dying(self):
        self.jump(9)
        self.state = "dying"
        self.img_file = self.sprite_imgs["dying"]
        self.frame_sizes = self.cell_frames["dying"]

    def update(self, game): # thay đổi chỉ số theo trạng thái
        last = self.rect.copy()
        new = self.accept_gravity(last)
        self.rect = new

        if self.state == 'dying':
            self.vx = 0
            if self.rect.bottom > WIN_HEIGHT:
                # self.state = 'reborn'
                game.restart()
            self.set_sprite(0)
            return

        # if self.state == 'reborn':
        #     self.reborn(game)
        #     return

        for sprite in game.triggers_group.sprites():
            if hasattr(sprite,'blocker') and sprite.rect.colliderect(new):
                value_blocker = sprite.blocker
                direct_mario_colled_obj = ""
                if 'l' in value_blocker and last.right <= sprite.rect.left and new.right > sprite.rect.left:
                    new.right = sprite.rect.left
                    self.vx = 0
                    direct_mario_colled_obj += 'r'

                if 'r' in value_blocker and last.left >= sprite.rect.right and new.left < sprite.rect.right:
                    new.left = sprite.rect.right
                    self.vx = 0
                    direct_mario_colled_obj += 'l'

                if 't' in value_blocker and last.bottom <= sprite.rect.top and new.bottom > sprite.rect.top:
                    new.bottom = sprite.rect.top
                    self.vy = 0
                    direct_mario_colled_obj += 'b'
                    self.v_state = "resting"

        
                if 'b' in value_blocker and last.top >= sprite.rect.bottom and new.top < sprite.rect.bottom:
                    new.top = sprite.rect.bottom
                    self.vy = 0
                    direct_mario_colled_obj += 't'

                if direct_mario_colled_obj != '':
                    self.collision_with_obj( sprite, direct_mario_colled_obj)
                elif (type(sprite).__name__ == "Turtlee" and sprite.live > 0) or (type(sprite).__name__ == "Flower" and sprite.v_facing == "up"):
                    self.get_hit()
                if self.state == 'dying':
                    return

        if self.rect.bottom > WIN_HEIGHT - 40 and self.state != 'dying':
            self.go_dying()
            return

        

        if self.state == 'invicible':
            self.time_invi -= 1
            if self.time_invi % 10 == 1:
                self.grow_up('medium',2)
            else:
                self.grow_up('small')
            if self.time_invi == 0:
                self.back_to_normal()

        # if self.state == 'dying':/

        if self.v_state == 'jumping':
            self.set_sprite(self.JUMP)
        else:
            if self.h_state == 'running':
                super().update(game)
            elif self.h_state == 'standing':
                self.set_sprite(self.STAND)
            

    def collision_with_obj(self, obj, direct): 
        type_obj = type(obj).__name__

        if type_obj == 'Coinbox':
            if obj.visible == False:
                    obj.visible = True
            elif 't' in direct and obj.count > 0:
                obj.get_hit()

        elif type_obj == 'Brick':
            if obj.visible == False:
                    obj.visible = True
            elif 't' in direct:
                obj.get_hit(self.size)
        
        elif type_obj == 'Turtlee':
            if obj.h_state == 'running':
                if 'b' in direct:
                    obj.get_hit()
                    self.jump(9)
                else:
                    self.get_hit()
            elif obj.h_state == 'standing': 
                if self.rect.centerx < obj.rect.centerx:
                    direct_shell_run = 'r'
                else:
                    direct_shell_run = 'l'
                obj.shell_running(direct_shell_run,self.rect)
