import math
import pygame 
import config

class Spritebase(pygame.sprite.Sprite):

    img_file = ""
    FRAME_WIDTH = 0
    FRAME_HEIGHT = 0
    PADDING = 1
    frame_sizes = None # Nếu kích thước frame giống nhau thì None
    frame_index = 0 # 
    FRAMES = [] # chứa index frame có thể thay đổi khi ở cùng 1 trạng thái 
    opacity = 255 # độ mờ cho ảnh RGBA and map size Mario   

    v_state = "resting"
    h_state = "standing"

    v_facing = "up"
    h_facing = "right"

    vx = 0
    vy = 0

    rect = None

    GRAVITY = 0.4
    MAX_VX = 3  # Gia tốc phương x
    MAX_VY = 20

    def __init__(self, index, location, hidden = True, *group):
        if group:
            super().__init__(group)
        else: 
            super().__init__()
        if index == -1: return
        self.set_visible(hidden)
        self.init_image_and_position(index, location)

    def init_image_and_position(self,index,locaion):
        self.set_sprite(index)
        self.rect = self.image.get_rect()
        self.rect.topleft = locaion

    def draw(self, screen, offset):
        if hasattr(self,'visible'):
            if self.visible == False: 
                return
        screen.blit(self.image, self.rect.topleft - offset)

    def set_blocker(self, value_blocker):
        self.blocker = value_blocker

    def jump(self,speed):
        self.vy = -speed
        self.v_state = 'jumping'

    def accept_gravity(self,last): 
        if abs(self.vx) > self.MAX_VX:
            self.vx = math.copysign(self.MAX_VX, self.vx)
        if abs(self.vy) > self.MAX_VY:
            self.vy = math.copysign(self.MAX_VY, self.vy)
        dy = self.vy
        dx = self.vx
        self.vy += self.GRAVITY
        new = last.move(dx, dy)
        return new

    def set_visible(self, hidden):
        self.visible = hidden

    def update(self, game):
        if game.time_step % self.ANIMATION_INTERVAL == 0:
            self.frame_index +=1
            self.frame_index  %= len(self.FRAMES)
            self.set_sprite(self.FRAMES[self.frame_index])

    def set_sprite(self,index):
        self.image = None
        img, cached = config.get_image_and_sprite(self.img_file)
        key_name = "_".join(map(str,[index, 255])) # opacity = 255
        if key_name not in cached : 
            clip_rect = self.get_clip_rect(index)
            _surface = pygame.Surface( clip_rect.size, pygame.SRCALPHA)
            _surface.blit(img, (0,0), clip_rect)
            # _surface.fill( (255,255,255,self.opacity), None, pygame.BLEND_RGB_MULT)
            cached[key_name] = _surface

        self.image = cached[key_name]
        config.sprites_pool[self.img_file][key_name] = self.image
        if self.rect and self.rect.size != self.image.get_rect().size:
                self.rect.size = self.image.get_rect().size

        if self.h_facing == "left":
            self.image = pygame.transform.flip(self.image,True,False)

    
    def get_clip_rect(self,index):
        left = 0
        if self.frame_sizes == None:
            left = (self.FRAME_WIDTH + self.PADDING) * index
            width, height = self.FRAME_WIDTH, self.FRAME_HEIGHT
        else:
            for i in range(index):
                left += self.frame_sizes[index][0] 
                if i>0: left += self.PADDING
            width, height = self.frame_sizes[index]

        return pygame.Rect(left, 0, width, height)



class Tile(Spritebase):

    def __init__(self,pos,surf,groups):
        super().__init__(-1,pos,True,groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)   

    def update(self, game):
        return 
        