import os
import time
import win32console
import win32con
from ..engine import Server
from ..engine.config import FRAME_PER_SECONDS
from .command import Command
from .screen import Screen


class Game:
    def __init__(self, command: Command, screen: Screen, server: Server):
        self.__command = command
        self.__screen = screen
        self.__server = server
        
        self.__console = win32console.CreateConsoleScreenBuffer(DesiredAccess = win32con.GENERIC_READ | win32con.GENERIC_WRITE, ShareMode=0, SecurityAttributes=None, Flags=1)
        self.__console.SetConsoleActiveScreenBuffer()
        self.__server.load_map_file(
            f'{os.path.dirname(__file__)}/../maps_pattern/map_1_level_1.txt')
    
        self.__frame_count = 0


    def start(self):
        self.__frame_count += 1
        loop_time = (1 / FRAME_PER_SECONDS)
        # self.__server.start_game()
        delta_time = loop_time
        self.__screen.draw_hud(self.__console)
        while 1:
            start_time = time.time()
            self.__command.apply(self.__server)
            self.__server.update(loop_time)
            state = self.__server.get_player_state("123")
            self.__screen.draw(self.__console, state)
            end_time = time.time()
            delta_time = end_time - start_time
            if delta_time < loop_time:
                time.sleep(loop_time - delta_time)
                delta_time = loop_time
            win32console.SetConsoleTitle(f'Pyfenstein3d - frame: {"%04.1f"%(1/delta_time)} - health: {"%03.0f"%state.health} - ammor: {"%03.0f"%state.ammo} - score: {state.score}')

