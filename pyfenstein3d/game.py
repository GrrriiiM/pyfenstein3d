import os
import math
from pynput import keyboard
import numpy as np
from PIL import Image
from threading import Thread
from engine import Server
from engine import FieldOfView
from engine.config import RAY_COUNT


class Game:
    def __init__(self):
        self.__walls_img = Image.open(
            f'{os.path.dirname(__file__)}/imgs/walls.png')
        self.__walls_img.load()
        self.__walls_img = np.asarray(self.__walls_img, dtype="int32")
        self.__server = Server()
        self.__server.load_map_file(
            f'{os.path.dirname(__file__)}/maps_pattern/map_1_level_1.txt')
        self.__server.start_game()
        self.__screen_h = 80
        self.__screen_w = 150
        self.__frame_count = 0
        self.__listener = keyboard.Listener(
            on_press=self.__on_press,
            on_release=self.__on_release)
        self.__listener.start()
        self.__thread = Thread(target=self.__draw)
        self.__thread.start()

    def __draw(self):
        while True:
            pixel_template = "\033[48;2;{};{};{}m  "
            state = self.__server.get_player_state("123")
            fov = get_fov(state["fov"])
            screen = None
            for i in range(RAY_COUNT):
                ray = fov.rays[i]
                if ray.wall is None:
                    continue
                img_h = math.floor((self.__screen_h * 5) / (ray.dist))
                img_x = math.floor(
                    (((ray.wall.type_id % 3) * 2) + ray.offset) * 64)
                if ray.is_vertical:
                    img_x += 64
                img_y = math.floor(ray.wall.type_id / 3) * 64
                wall_img = self.__walls_img[img_y:img_y + 64, img_x:img_x+1, :]
                img_factor = img_h / self.__screen_h
                img_margin = math.floor((self.__screen_h - img_h) / 2)

                pixels = []
                for h in range(self.__screen_h):
                    _h = math.floor((h / img_factor-img_margin));
                    if h < img_margin or _h >= 64:
                        pixels.append([0, 0, 0])
                    else:
                        pixel = wall_img[_h][0]
                        pixels.append(pixel)

                # pixels = np.asarray([pixels])
                if screen is None:
                    screen = [pixels]
                else:
                    screen.append(pixels)
            if screen is not None:
                print("\033[%d;%dH" % (0, 3))
                for y in range(self.__screen_h):
                    for x in range(self.__screen_w):
                        pixel = screen[x][y]
                        print(pixel_template.format(pixel[0], pixel[1], pixel[2]), end="")
                    print()

    def __on_press(self, key):
        try:
            if key.char == "w":
                self.__server.player_start_moving_front("123")
            elif key.char == "a":
                self.__server.player_start_moving_left("123")
            elif key.char == "s":
                self.__server.player_start_moving_back("123")
            elif key.char == "d":
                self.__server.player_start_moving_right("123")
        except:
            pass
            # print('special key {0} pressed'.format(
            #     key))

    def __on_release(self, key):
        try:
            if key.char == "w":
                self.__server.player_stop_moving_front("123")
            elif key.char == "a":
                self.__server.player_stop_moving_left("123")
            elif key.char == "s":
                self.__server.player_stop_moving_back("123")
            elif key.char == "d":
                self.__server.player_stop_moving_right("123")
            if key == keyboard.Key.esc:
                # Stop listener
                return False
        except:
            pass


def get_fov(fov) -> FieldOfView:
    return fov
