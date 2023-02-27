import pygame
import pytmx

WIDTH = 860
HEIGHT = 560
FPS = 60

class Tile(pygame.sprite.Sprite):
    def __init__(self,pos,surf,groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)


pygame.init()
pygame.display.set_caption("T-REX")

screen = pygame.display.set_mode((WIDTH,HEIGHT))
screen.fill((0,140,230))
clock = pygame.time.Clock()

tmx_data = pytmx.load_pygame("./Tiled/untitled.tmx")

cell_blockers = {}

for cell in tmx_data.get_layer_by_name('Triggers'):
    if 'blocker' in cell.properties:
        print(dir(cell))
        print(cell.name)
        print(cell.parent)
        print(cell.template)
        print(cell.type)

key_name = "_".join(map(str,[1, 254])) # opacity = 255


sprite_group = pygame.sprite.Group()
for layer in tmx_data.layers:
    if (hasattr(layer,'data')): # get tile layers 
        for x,y,surf in layer.tiles():
            pos = (x*20,y*14)
            # print(pos,surf)
            Tile(pos,surf,sprite_group)


running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    sprite_group.draw(screen)
    pygame.display.flip()

pygame.quit()    
