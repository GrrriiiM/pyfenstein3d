import keyboard
from ..engine import Server

class Command:

    def apply(self, server: Server):
        server.player_stop_turning_left("123")
        server.player_stop_turning_right("123")
        server.player_stop_shooting("123")
        server.player_stop_moving_front("123")
        server.player_stop_moving_back("123")
        server.player_stop_moving_left("123")
        server.player_stop_moving_right("123")
        server.player_stop_interacting("123")
            
        if keyboard.is_pressed("left"):
            server.player_start_turning_left("123")
        if keyboard.is_pressed("right"):
            server.player_start_turning_right("123")
        if keyboard.is_pressed("up"):
            server.player_start_shooting("123")
        if keyboard.is_pressed("w"):
            server.player_start_moving_front("123")
        if keyboard.is_pressed("s"):
            server.player_start_moving_back("123")
        if keyboard.is_pressed("a"):
            server.player_start_moving_left("123")
        if keyboard.is_pressed("d"):
            server.player_start_moving_right("123")
        if keyboard.is_pressed(" "):
            server.player_start_interacting("123")
