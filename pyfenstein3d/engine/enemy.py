import math
from .vector2d import Vector2d
from .person import Person
from .field_of_view import FieldOfView
from .vector2d import Vector2d

class Enemy(Person):
    def __init__(self, vector_x: float, vector_y: float, type_id: int, fov: FieldOfView):
        super().__init__(vector_x, vector_y, type_id, fov)
        self.__health = 100

    def _get_bounds(self, fov_ang: float):
        bounds = []
        pos = self._vector2d ** -fov_ang
        bounds.append(Vector2d(pos.x - 0.5, pos.y) ** fov_ang)
        bounds.append(Vector2d(pos.x + 0.5, pos.y) ** fov_ang)
        return bounds

    def get_state(self, player):
        ang = (Vector2d(player.x, player.y) - Vector2d(self.x, self.y)).ang + math.pi
        ang = (ang - (self.fov_ang + math.pi) + (math.pi * 2)) % (math.pi * 2)
        i = math.pi / 4
        for s in range(8):
            if ang < (s + 0.5) * i:
                return s
        return 0

    @staticmethod
    def create(vector_x: float, vector_y: float, type_id: int):
        if type_id == 131:
            return EnemyDog(vector_x, vector_y, FieldOfView(0))
        return EnemyGuard(vector_x, vector_y, FieldOfView(0))

class EnemyGuard(Enemy):
    def __init__(self, vector_x: float, vector_y: float, fov: FieldOfView):
        super().__init__(vector_x, vector_y, 130, fov)

class EnemyDog(Enemy):
    def __init__(self, vector_x: float, vector_y: float, fov: FieldOfView):
        super().__init__(vector_x, vector_y, 131, fov)
