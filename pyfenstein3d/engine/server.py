import time
import asyncio
from threading import Thread
from .map2d import Map2d
from .config import FRAME_PER_SECONDS

class Server:
    def __init__(self):
        self.__map2d: Map2d
        self.__game_is_running = False
        self.__thread: Thread
        self.frame_count = 0

    def load_map_file(self, file_path:str):
        pattern: str
        with open(file_path, "r") as file:
            pattern = file.readlines()
        self.__map2d = Map2d.create_with_pattern(pattern)

    def start_game(self):
        if not self.__game_is_running:
            # if self.__map2d is None:
            #     raise ValueError("Map2d")
            self.__game_is_running = True
            self.__thread = Thread(target=self.__loop)
            self.__thread.start()

    # def __start_loop(self):
    #     asyncio.set_event_loop(self.__loop)
    #     self.__loop.run_until_complete(self.__clock())
    #     self.__thread.

    def stop_game(self):
        self.__game_is_running = False

    def get_state(self, player_id: str):
        return {
            "fov": self.__map2d.get_player(player_id).fov
        }

    def player_start_moving_front(self, player_id: str):
        self.__map2d.get_player(player_id).is_moving_front = True
    def player_start_moving_back(self, player_id: str):
        self.__map2d.get_player(player_id).is_moving_back = True
    def player_start_moving_right(self, player_id: str):
        self.__map2d.get_player(player_id).is_moving_right = True
    def player_start_moving_left(self, player_id: str):
        self.__map2d.get_player(player_id).is_moving_left = True
    def player_start_turning_right(self, player_id: str):
        self.__map2d.get_player(player_id).is_turning_right = True
    def player_start_turning_left(self, player_id: str):
        self.__map2d.get_player(player_id).is_turning_left = True

    def player_stop_moving_front(self, player_id: str):
        self.__map2d.get_player(player_id).is_moving_front = False
    def player_stop_moving_back(self, player_id: str):
        self.__map2d.get_player(player_id).is_moving_back = False
    def player_stop_moving_right(self, player_id: str):
        self.__map2d.get_player(player_id).is_moving_right = False
    def player_stop_moving_left(self, player_id: str):
        self.__map2d.get_player(player_id).is_moving_left = False
    def player_stop_turning_right(self, player_id: str):
        self.__map2d.get_player(player_id).is_turning_right = False
    def player_stop_turning_left(self, player_id: str):
        self.__map2d.get_player(player_id).is_turning_left = False


    def __loop(self):
        self.frame_count += 1
        loop_time = (1000 / FRAME_PER_SECONDS) / 1000
        while True:
            if not self.__game_is_running:
                break
            start_time = time.time()
            # self.__map2d.update()
            print(start_time)
            end_time = time.time()
            delta_time = end_time - start_time
            if delta_time < loop_time:
                time.sleep(1)#loop_time - delta_time)
