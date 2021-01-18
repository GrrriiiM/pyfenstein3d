from .vector2d import Vector2d
from .block import Block

class Item(Block):
    def __init__(self, vector_x: float, vector_y: float, type_id: int, is_solid: bool=False):
        super().__init__(vector_x, vector_y, type_id, is_solid, False)

    def _get_bounds(self, fov_ang: float):
        bounds = []
        pos = self._vector2d ** -fov_ang
        bounds.append(Vector2d(pos.x - 0.5, pos.y) ** fov_ang)
        bounds.append(Vector2d(pos.x + 0.5, pos.y) ** fov_ang)
        return bounds

    def touch(self, player):
        pass
