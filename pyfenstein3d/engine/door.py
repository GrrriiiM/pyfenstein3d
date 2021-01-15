import math
from .block import Block
from .vector2d import Vector2d
from .config import DOOR_OPEN_VELOCITY
from .config import DOOR_INTERVAL_CLOSE
from .animation import Animation

class Door(Block):
    def __init__(self, x: float, y: float, type_id: int, is_vertical: bool):
        super().__init__(x, y, type_id, True)
        self.__is_vertical = is_vertical
        self._is_solid = True
        self.__is_opened = False
        self.__is_opening = False
        self.__is_closing = False
        self.__original_x = x
        self.__original_y = y
        self.__closing_interval = 0
        self.__animations = {
            "open": Animation(DOOR_OPEN_VELOCITY, self.__on_opening_animate, self.__on_opening_animate_end),
            "wait": Animation(DOOR_INTERVAL_CLOSE, on_animate_end=self.__on_waiting_animate_end),
            "close": Animation(DOOR_OPEN_VELOCITY, self.__on_closing_animate, self.__on_closing_animate_end)
        }


    @property
    def is_vertical(self):
        return self.__is_vertical

    def __open(self):
        self.__animations["open"].start()

    def __close(self):
        self._is_solid = True
        self.__animations["close"].start()

    def __on_opening_animate(self, factor):
        vector = Vector2d(factor if not self.is_vertical else 0, factor if self.is_vertical else 0)
        self._vector2d = Vector2d(self.__original_x, self.__original_y) - vector

    def __on_opening_animate_end(self):
        self.__is_opening = False
        self.__is_opened = True
        self._is_solid = False
        self.__animations["wait"].start()

    def __on_waiting_animate_end(self):
        self.__close()

    def __on_closing_animate(self, factor):
        vector = Vector2d(1 - factor if not self.is_vertical else 0, 1 - factor if self.is_vertical else 0)
        self._vector2d = Vector2d(self.__original_x, self.__original_y) - vector

    def __on_closing_animate_end(self):
        self.__is_closing = False
        self.__is_opened = False


    def _get_bounds(self, fov_ang: float):
        bounds = []
        bounds.append(self._vector2d)
        bounds.append(self._vector2d + Vector2d(1 if not self.__is_vertical else 0, 1 if self.__is_vertical else 0))
        return bounds

    def update(self, delta_time: float, persons: []):
        for anim in self.__animations.values():
            anim.update(delta_time)
                
    def interacted(self):
        if not self.__is_opening and not self.__is_closing:
            if not self.__is_opened:
                self.__open()
