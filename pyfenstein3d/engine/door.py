import math
from .block import Block
from .vector2d import Vector2d
from .config import DOOR_OPEN_VELOCITY
from .config import DOOR_INTERVAL_CLOSE

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


    @property
    def is_vertical(self):
        return self.__is_vertical

    def _get_bounds(self, fov_ang: float):
        bounds = []
        bounds.append(self._vector2d)
        bounds.append(self._vector2d + Vector2d(1 if not self.__is_vertical else 0, 1 if self.__is_vertical else 0))
        return bounds

    def update(self, persons: []):
        if self.__is_opening:
            if self.is_vertical:
                next_y = self.y - DOOR_OPEN_VELOCITY
                if next_y <= self.__original_y - 1:
                    next_y = self.__original_y - 1
                    self._is_solid = False
                    self.__is_opening = False
                    self.__is_opened = True
                    self.__closing_interval = 1
                self._vector2d = Vector2d(self.x, next_y)
            else:
                next_x = self.x - DOOR_OPEN_VELOCITY
                if next_x <= self.__original_x - 1:
                    next_x = self.__original_x - 1
                    self._is_solid = False
                    self.__is_opening = False
                    self.__is_opened = True
                    self.__closing_interval = 1
                self._vector2d = Vector2d(next_x, self.y)
        elif self.__is_closing:
            if self.is_vertical:
                next_y = self.y + DOOR_OPEN_VELOCITY
                if next_y >= self.__original_y:
                    next_y = self.__original_y
                    self.__is_closing = False
                    self.__is_opened = False
                self._vector2d = Vector2d(self.x, next_y)
            else:
                next_x = self.x + DOOR_OPEN_VELOCITY
                if next_x >= self.__original_x:
                    next_x = self.__original_x
                    self.__is_closing = False
                    self.__is_opened = False
                self._vector2d = Vector2d(next_x, self.y)
        elif self.__closing_interval > 0:
            if any([person for person in persons if math.floor(person.x) == math.floor(self.__original_x) and math.floor(person.y) == math.floor(self.__original_y)]):
                self.__closing_interval = 1
            self.__closing_interval -= DOOR_INTERVAL_CLOSE
            if self.__closing_interval <= 0:
                self.__closing_interval = 0
                self.__is_closing = True
                self._is_solid = True
        
    def interacted(self):
        if not self.__is_opening and not self.__is_closing:
            if not self.__is_opened:
                self.__is_opening = True
