from .block import Block
from .vector2d import Vector2d

class Door(Block):
    def __init__(self, x: float, y: float, type_id: int, is_vertical: bool):
        super().__init__(x, y, type_id, False)
        self.__is_vertical = is_vertical

    @property
    def is_vertical(self):
        return self.__is_vertical

    def _get_bounds(self, fov_ang: float):
        bounds = []
        bounds.append(self._vector2d)
        bounds.append(self._vector2d + Vector2d(1 if not self.__is_vertical else 0, 1 if self.__is_vertical else 0))
        return bounds
