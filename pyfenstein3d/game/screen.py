import os
import math
import numpy as np
from PIL import Image as pil_image
from ..engine import FieldOfView
from ..engine import Ray
from ..engine import Player
from ..engine.config import RAY_COUNT
from .image import Image

class Screen:
    def __init__(self, images: Image):
        self.__images = images
        self.__hud_img = pil_image.open(
            f'{os.path.dirname(__file__)}/../imgs/hud.png')
        self.__hud_img.load()
        self.__hud_img = np.asarray(self.__hud_img, dtype="int32")
        self.__screen_w = RAY_COUNT
        self.__screen_h = math.floor(RAY_COUNT * 0.5)
        self.__hud_h = math.floor(RAY_COUNT / 8)
        self.__image_size = 64
        self.__pixel_template = "\033[48;2;{};{};{}m  "
        self.__image = None


    def draw(self, console, player: Player):
        pixel_matrix = self.create_pixel_matrix(player)
        console.WriteConsole("\033[0;0H")
        console_text = []
        for pixel_h in range(self.__screen_h):
            console_line = []
            for pixel_w in range(self.__screen_w):
                pixel = pixel_matrix[pixel_h][pixel_w]
                console_pixel = self.__pixel_template.format(pixel[0], pixel[1], pixel[2])
                console_line.append(console_pixel)
            console_text.append("".join(console_line))
        console.WriteConsole("\n".join(console_text))

    def create_pixel_matrix(self, player: Player):
        fov = player.fov
        img = Image.create_background(self.__screen_w, self.__screen_h)
        for i in range(self.__screen_w):
            ray = fov.rays[i]
            if ray.type_id is None:
                continue
            if ray.dist_adjusted > 0:
                height = round(self.__screen_h * 2 / ray.dist_adjusted)
                offset = math.floor(ray.offset * 64)
                img_column = self.__images.get_column(ray.type_id, offset, height, 1 if ray.is_vertical else 0)
                img.paste(img_column, (i, math.floor(self.__screen_h / 2 - height / 2)))
                list_items = list(ray.items + ray.doors)
                if len(list_items) > 0:
                    list_items.sort(key=lambda i: i.dist, reverse=True)
                    for ray_item in list_items:
                        if ray_item.dist > 0.001:
                            height = round(self.__screen_h * 2 / ray_item.dist)
                            if type(ray_item).__name__ == "RayDoor":
                                offset = math.floor(ray_item.offset * 64)
                                img_column = self.__images.get_column(49, offset, height, ray_item.state)
                            else:
                                offset = math.floor((ray_item.offset + 0.5) * 64)
                                img_column = self.__images.get_column(ray_item.type_id, offset, height, ray_item.state)
                            img.paste(img_column, (i, math.floor(self.__screen_h / 2 - height / 2)), img_column)
        img_weapon = self.__images.get(player.weapon.type_id)
        if player.weapon.shoot_animation.is_animating:
            if player.weapon.shoot_animation.factor < 0.2:
                img_weapon = self.__images.get(player.weapon.type_id, state=1)
            elif player.weapon.shoot_animation.factor < 0.3:
                img_weapon = self.__images.get(player.weapon.type_id, state=2)
            elif player.weapon.shoot_animation.factor < 0.6:
                img_weapon = self.__images.get(player.weapon.type_id, state=3)
            else:
                img_weapon = self.__images.get(player.weapon.type_id, state=4)
        img.paste(img_weapon, (round(self.__screen_w / 2 - img_weapon.width / 2), self.__screen_h - img_weapon.height), img_weapon)
        return np.asarray(img)

    def draw_hud(self, console):
        console.WriteConsole(f"\033[{self.__screen_h};0H")
        pixel_matrix = self.get_image_hud()
        img_h = 40
        img_factor = img_h / (RAY_COUNT / 8)
        console_text = []
        for pixel_h in range(self.__hud_h):
            console_line = []
            for pixel_w in range(self.__screen_w):
                pixel = pixel_matrix[math.floor(pixel_h * img_factor)][math.floor(pixel_w * img_factor)]
                console_pixel = self.__pixel_template.format(pixel[0], pixel[1], pixel[2])
                console_line.append(console_pixel)
            console_text.append("".join(console_line))
        console.WriteConsole("\n".join(console_text))


    def get_image_hud(self):
        return self.__hud_img[:40, :, :]