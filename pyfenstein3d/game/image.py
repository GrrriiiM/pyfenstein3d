import math
import os
import numpy as np
from PIL import Image as pil


class Image():
    def __init__(self):
        self.__images = [None] * 255
        self.__add_wall()
        self.__add_items()
        self.__add_weapons()
        self.__add_enemy_guard()
        self.__add_enemy_dog()

    def __add_wall(self):
        img = pil.open(f'{os.path.dirname(__file__)}/../imgs/walls.png').convert('RGBA')
        img_size = 64
        for i in range(55):
            img_x = i % 3 * 2 * img_size
            img_y = math.floor(i / 3) * img_size
            self.__images[i] = []
            self.__images[i].append(pil.Image.crop(img, (img_x, img_y, img_x + img_size, img_y + img_size)));
            self.__images[i].append(pil.Image.crop(img, (img_x + img_size, img_y, img_x + img_size * 2 ,img_y + img_size)));

    def __add_items(self):
        img = pil.open(f'{os.path.dirname(__file__)}/../imgs/items.png').convert('RGBA')
        img_size = 64
        for i in range(64):
            img_x = (i % 5 * img_size + i % 5)
            img_y = math.floor(i / 5) * img_size + math.floor(i / 5)
            self.__images[56 + i] = []
            self.__images[56 + i].append(pil.Image.crop(img, (img_x, img_y, img_x + img_size, img_y + img_size)));

    def __add_weapons(self):
        img = pil.open(f'{os.path.dirname(__file__)}/../imgs/weapons.png').convert('RGBA')
        img_size = 64
        for i in range(4):
            img_x = 0
            img_y = i * img_size
            self.__images[120 + i] = []
            for j in range(5):
                x1 = j + img_size * j
                x2 = j + img_size * (j + 1)
                self.__images[120 + i].append(pil.Image.crop(img, (x1, img_y, x2, img_y + img_size)));

    def __add_enemy_guard(self):
        img = pil.open(f'{os.path.dirname(__file__)}/../imgs/enemy-guard.png').convert('RGBA')
        img_size = 64
        self.__images[130] = []
        for i in range(7):
            img_y = img_size * i + i
            for j in range(8):
                img_x = img_size * j + j
                self.__images[130].append(pil.Image.crop(img, (img_x, img_y, img_x + img_size, img_y + img_size)));

    def __add_enemy_dog(self):
        img = pil.open(f'{os.path.dirname(__file__)}/../imgs/enemy-dog.png').convert('RGBA')
        img_size = 64
        self.__images[131] = []
        for i in range(7):
            img_y = img_size * i + i
            for j in range(8):
                img_x = img_size * j + j
                self.__images[131].append(pil.Image.crop(img, (img_x, img_y, img_x + img_size, img_y + img_size)));


    def get(self, type_id: int, width=64, height=64, state=0):
        img = self.__images[type_id][state]
        if width != 64 or height != 64:
            img = pil.Image.resize(img, (width, height))
        return img

    def get_column(self, type_id: int, col: int, height=64.0, state=0):
        img = self.__images[type_id][state]
        img = pil.Image.crop(img, (col, 0, col + 1, 64))
        img = pil.Image.resize(img, (1, round(height)), pil.NEAREST)
        return img

    @staticmethod
    def create_background(width, height):
        img = pil.new("RGBA", (width, height))
        pixels = [(30, 30, 30, 255)] * math.floor(width * height / 2)
        pixels += [(100, 100, 100, 255)] * math.ceil(width * height / 2)
        img.putdata(pixels)
        return img
