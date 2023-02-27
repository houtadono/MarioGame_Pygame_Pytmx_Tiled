import pygame
import config

class Sprites_group(pygame.sprite.Group):

    def __init__(self):
        super(Sprites_group,self).__init__()

    def draw(self,sceen,offset):
        for sprite in self.sprites():
            sprite.draw(sceen, offset) 

    def update(self,game):
        for sprite in self.sprites():
            sprite.update(game)

