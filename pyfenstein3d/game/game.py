import os
import time
import ctypes
import win32console
import win32con
from ..engine import Server
from ..engine.config import FRAME_PER_SECONDS
from .command import Command
from .screen import Screen
from .console_manager import resize
from .console_manager import set_font


class Game:
    def __init__(self, command: Command, screen: Screen, server: Server):
        self.prepare_console();
        self.__command = command
        self.__screen = screen
        self.__server = server
        
        self.__console = win32console.CreateConsoleScreenBuffer(DesiredAccess = win32con.GENERIC_READ | win32con.GENERIC_WRITE, ShareMode=0, SecurityAttributes=None, Flags=1)
        self.__console.SetConsoleActiveScreenBuffer()
        self.__server.load_map_file(
            # f'{os.path.dirname(__file__)}/../maps_pattern/map_test.txt')
            f'{os.path.dirname(__file__)}/../maps_pattern/map_1_level_1.txt')
    
        self.__frame_count = 0

    def prepare_console(self):
        os.system("cls")
        print("COMANDOS")
        print("- Andar para frente: W")
        print("- Andar para trás: S")
        print("- Andar para esquerda: A")
        print("- Andar para direita: D")
        print("- Virar para esquerda: Seta esquerda")
        print("- Virar para direita: Seta direta")
        print("- Atirar: Seta cima")
        print("- Abrir porta: Espaço")
        print()
        print("As configurações do seu console serão alteradas:")
        print("LARGURA: 200")
        print("ALTURA: 62")
        print("FONTE: Consolas 5px")
        print()
        print("Pressione ENTER tecla para começar")
        input()
        set_font()
        resize(200, 62)
        os.system("cls")


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

import sys
from ctypes import POINTER, WinDLL, Structure, sizeof, byref
from ctypes.wintypes import BOOL, SHORT, WCHAR, UINT, ULONG, DWORD, HANDLE


LF_FACESIZE = 32
STD_OUTPUT_HANDLE = -11


class COORD(Structure):
    _fields_ = [
        ("X", SHORT),
        ("Y", SHORT),
    ]


class CONSOLE_FONT_INFOEX(Structure):
    _fields_ = [
        ("cbSize", ULONG),
        ("nFont", DWORD),
        ("dwFontSize", COORD),
        ("FontFamily", UINT),
        ("FontWeight", UINT),
        ("FaceName", WCHAR * LF_FACESIZE)
    ]


kernel32_dll = WinDLL("kernel32.dll")

get_last_error_func = kernel32_dll.GetLastError
get_last_error_func.argtypes = []
get_last_error_func.restype = DWORD

get_std_handle_func = kernel32_dll.GetStdHandle
get_std_handle_func.argtypes = [DWORD]
get_std_handle_func.restype = HANDLE

get_current_console_font_ex_func = kernel32_dll.GetCurrentConsoleFontEx
get_current_console_font_ex_func.argtypes = [HANDLE, BOOL, POINTER(CONSOLE_FONT_INFOEX)]
get_current_console_font_ex_func.restype = BOOL

set_current_console_font_ex_func = kernel32_dll.SetCurrentConsoleFontEx
set_current_console_font_ex_func.argtypes = [HANDLE, BOOL, POINTER(CONSOLE_FONT_INFOEX)]
set_current_console_font_ex_func.restype = BOOL

