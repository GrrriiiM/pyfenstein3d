import os
import math
import numpy as np
from PIL import Image
from engine import FieldOfView
from engine.config import RAY_COUNT

class Screen:
    def __init__(self):
        self.__walls_img = Image.open(
            f'{os.path.dirname(__file__)}/imgs/walls.png')
        self.__walls_img.load()
        self.__walls_img = np.asarray(self.__walls_img, dtype="int32")
        self.__screen_w = RAY_COUNT
        self.__screen_h = math.floor(RAY_COUNT * 0.5)
        self.__wall_size = 64
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

    def create_pixel_column(self, ray):
        wall_img_column = self.get_image_column(ray.wall.type_id, ray.dist, ray.offset, ray.is_vertical)
        img_h = math.floor((self.__screen_h * 2) / (ray.dist + 0.0000000001))
        img_factor = (self.__screen_h / img_h) / (self.__screen_h / self.__wall_size)
        img_margin = math.floor(self.__screen_h / 2 - img_h/2)

        pixel_column = []
        for pixel_h in range(self.__screen_h):
            img_pixel_h = math.floor((pixel_h - img_margin) * img_factor)
            if img_pixel_h < 0:
                pixel_column.append([30, 30, 30])
            elif img_pixel_h >= 64:
                pixel_column.append([100, 100, 100])
            else:
                pixel_column.append(wall_img_column[img_pixel_h][0])
            
        return pixel_column

    def get_image_column(self, type_id, dist, offset, is_vertical):
        img_x = math.floor((((type_id % 3) * 2) + offset) * self.__wall_size)
        if is_vertical:
            img_x += self.__wall_size
        img_y = math.floor(type_id / 3) * self.__wall_size
        wall_img = self.__walls_img[img_y:img_y + self.__wall_size, img_x:img_x+1, :]
        return wall_img


