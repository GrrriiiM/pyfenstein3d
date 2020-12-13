import os
import math
import numpy as np
from PIL import Image
from engine import FieldOfView
from engine import Ray
from engine.config import RAY_COUNT

class Screen:
    def __init__(self):
        self.__walls_img = Image.open(
            f'{os.path.dirname(__file__)}/imgs/walls.png')
        
        self.__walls_img.load()
        self.__walls_img = np.asarray(self.__walls_img, dtype="int32")
        self.__items_img = Image.open(
            f'{os.path.dirname(__file__)}/imgs/items.png')
        self.__items_img.load()
        self.__items_img = np.asarray(self.__items_img, dtype="int32")
        self.__screen_w = RAY_COUNT
        self.__screen_h = math.floor(RAY_COUNT * 0.5)
        self.__image_size = 64
        self.__pixel_template = "\033[48;2;{};{};{}m  "


    def draw(self, console, fov: FieldOfView):
        pixel_matrix = None
        for i in range(RAY_COUNT):
            ray = fov.rays[i]
            if ray.wall is None:
                continue
            pixel_column = self.create_pixel_column(ray)
            if pixel_matrix is None:
                pixel_matrix = [pixel_column]
            else:
                pixel_matrix.append(pixel_column)
        if pixel_matrix is not None:
            console.WriteConsole("\033[0;0H")
            consoel_text = []
            for pixel_h in range(self.__screen_h):
                console_line = []
                for pixel_w in range(self.__screen_w):
                    pixel = pixel_matrix[pixel_w][pixel_h]
                    console_pixel = self.__pixel_template.format(pixel[0], pixel[1], pixel[2])
                    console_line.append(console_pixel)
                consoel_text.append("".join(console_line))
            console.WriteConsole("\n".join(consoel_text))

    def create_pixel_column(self, ray: Ray):
        pixel_column = [[30, 30, 30]] * math.floor(RAY_COUNT / 2)
        pixel_column.extend([[100, 100, 100]] * math.ceil(RAY_COUNT / 2))
        self.draw_pixel_column_wall(pixel_column, ray)
        self.draw_pixel_column_item(pixel_column, ray)
        return pixel_column

    def draw_pixel_column_wall(self, pixel_column, ray: Ray):
        wall_img_column = self.get_image_wall_column(ray.wall.type_id, ray.offset, ray.is_vertical)
        img_h = math.floor((self.__screen_h * 2) / (ray.dist + 0.0000000001))
        img_factor = (self.__screen_h / img_h) / (self.__screen_h / self.__image_size)
        img_margin = math.floor(self.__screen_h / 2 - img_h/2)
        for pixel_h in range(self.__screen_h):
            img_pixel_h = math.floor((pixel_h - img_margin) * img_factor)
            if 64 > img_pixel_h >= 0:
                pixel_column[pixel_h] = wall_img_column[img_pixel_h][0]

    def draw_pixel_column_item(self, pixel_column, ray: Ray):
        list_items = list(ray.items)
        list_items.sort(key=lambda i: i.dist)
        for ray_item in list_items:
            item_img_column = self.get_image_item_column(ray_item.item.type_id, ray_item.offset)
            img_h = math.floor((self.__screen_h * 2) / (ray_item.dist + 0.0000000001))
            img_factor = (self.__screen_h / img_h) / (self.__screen_h / self.__image_size)
            img_margin = math.floor(self.__screen_h / 2 - img_h/2)
            for pixel_h in range(self.__screen_h):
                img_pixel_h = math.floor((pixel_h - img_margin) * img_factor)
                if self.__image_size > img_pixel_h >= 0:
                    if item_img_column[img_pixel_h].size > 0:
                        img_pixel = item_img_column[img_pixel_h][0]
                        if img_pixel[3] != 0:
                            pixel_column[pixel_h] = item_img_column[img_pixel_h][0]


    def get_image_wall_column(self, type_id, offset, is_vertical):
        offset = math.floor(offset * self.__image_size)
        img_wall = self.get_image_wall(type_id, is_vertical)
        return img_wall[:, offset:offset+1]

    def get_image_wall(self, type_id, is_vertical):
        img_x = type_id % 3 * 2 * self.__image_size
        if is_vertical:
            img_x += self.__image_size
        img_y = math.floor(type_id / 3) * self.__image_size
        wall_img = self.__walls_img[img_y:img_y + self.__image_size, img_x:img_x+self.__image_size, :]
        return wall_img



    def get_image_item_column(self, type_id, offset):
        offset = math.floor(offset * self.__image_size)
        img_wall = self.get_image_item(type_id)
        return img_wall[:, offset:offset+1]

    def get_image_item(self, type_id):
        type_id -= 56
        img_x = type_id % 5 * self.__image_size + type_id % 5
        img_y = math.floor(type_id / 5) * self.__image_size + math.floor(type_id / 5)
        img = self.__items_img[img_y:img_y + self.__image_size, img_x:img_x+self.__image_size, :]
        return img


