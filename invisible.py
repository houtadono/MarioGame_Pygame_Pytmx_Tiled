import pygame
import spritebase

class Invisible(pygame.sprite.Sprite):

    def __init__(self, value_blocker, rect, group):
        self.rect = rect
        self.blocker =  value_blocker
        super(Invisible,self).__init__(group)
    
    def draw(self, screen, pos):
        return 

    def update(self,game):
        return
    