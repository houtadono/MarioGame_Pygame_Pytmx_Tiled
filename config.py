import os
import pygame

WIN_WIDTH = 460
WIN_HEIGHT = 362

# WIN_WITDH = 1280
# WIN_HEIGHT = 650

TILE_WIDTH = 20
TILE_HEIGHT = 14

ZOOM = 3

FPS = 55

# RECT left mario size

image_path = ".\images"

images_pool = {} # chứa pygame image
sprites_pool = {} # chứa từng sprite tương ứng 

def get_image_and_sprite(img_file):
    if img_file not in images_pool.keys():
        images_pool[img_file] = load_image(img_file)
        sprites_pool[img_file] = {}
    return images_pool[img_file], sprites_pool[img_file]

def load_image(img_file):
    _path = os.path.join(image_path, img_file)
    return pygame.image.load(_path)

OFFSET_CAMERA = pygame.math.Vector2()
def set_camera(target):
    OFFSET_CAMERA.x = target.rect.x - WIN_WIDTH//2
    OFFSET_CAMERA.y = 0

sound_path = ".\sounds"
coinbox_sound = 'coinbox_up.ogg'

def play_sound(sound_file):
    _path = os.path.join(sound_path, sound_file)
    s = pygame.mixer.Sound(_path)
    s.play()

