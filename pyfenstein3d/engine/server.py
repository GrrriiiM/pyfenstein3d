import time
import asyncio
from threading import Thread
from .map2d import Map2d
from .config import FRAME_PER_SECONDS

class Server:
    def __init__(self):
        self.__map2d: Map2d
        self.__game_is_running = False
        self.__thread: Thread = None
        self.frame_count = 0
        self.__delta_time = 1 / FRAME_PER_SECONDS

    def load_map_file(self, file_path:str):
        pattern: str
        with open(file_path, "r") as file:
            pattern = "".join(file.readlines())
        self.__map2d = Map2d.create_with_pattern(pattern)

    def start_game(self):
        if not self.__game_is_running:
            # if self.__map2d is None:
            #     raise ValueError("Map2d")
            self.__game_is_running = True
            self.__thread = Thread(target=self.__loop)
            self.__thread.setDaemon(True)
            self.__thread.start()

    # def __start_loop(self):
    #     asyncio.set_event_loop(self.__loop)
    #     self.__loop.run_until_complete(self.__clock())
    #     self.__thread.

    def stop_game(self):
        self.__game_is_running = False
        if self.__thread is not None:
            self.__thread.join()

    def get_player_state(self, player_id: str):
        return self.__map2d.get_player(player_id)

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
    def player_start_interacting(self, player_id: str):
        self.__map2d.get_player(player_id).is_interacting = True
    def player_start_shooting(self, player_id: str):
        self.__map2d.get_player(player_id).weapon.is_shooting = True

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
    def player_stop_interacting(self, player_id: str):
        self.__map2d.get_player(player_id).is_interacting = False
    def player_stop_shooting(self, player_id: str):
        self.__map2d.get_player(player_id).weapon.is_shooting = False

    def update(self, delta_time):
        self.__delta_time = delta_time
        self.__map2d.update(self.__delta_time)

    def __loop(self):
        self.frame_count += 1
        loop_time = 1 / FRAME_PER_SECONDS
        while self.__game_is_running:
            start_time = time.time()
            self.update(loop_time)
            # print(start_time)
            end_time = time.time()
            self.__delta_time = end_time - start_time
            # time.sleep(1)
            if self.__delta_time < loop_time:
                time.sleep(loop_time - self.__delta_time)
            else:
                time.sleep(0.00000001)
