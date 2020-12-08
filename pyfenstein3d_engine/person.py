from .item import Item
from .vector2d import Vector2d
from .field_of_view import FieldOfView
from .config import PERSON_TURN_VELOCITY
from .config import PERSON_MOVEMENT_VELOCITY

class Person(Item):
    def __init__(self, vector_x: float, vector_y: float, type_id: int, fov: FieldOfView):
        super().__init__(vector_x, vector_y, type_id, True)
        self.__fov = fov
        self.__last_pos = self._vector2d.copy()
        self.is_turning_left = False
        self.is_turning_right = False
        self.is_moving_front = False
        self.is_moving_back = False
        self.is_moving_left = False
        self.is_moving_right = False

    @property
    def fov_ang(self):
        return self.__fov.ang

    def update(self):
        if self.is_turning_left:
            self.turn(-PERSON_TURN_VELOCITY)
        if self.is_turning_right:
            self.turn(PERSON_TURN_VELOCITY)
        movement_x = 0
        movement_y = 0
        movement_count = 0
        if self.is_moving_front:
            movement_x += PERSON_MOVEMENT_VELOCITY
            movement_count += 1
        if self.is_moving_back:
            movement_x -= PERSON_MOVEMENT_VELOCITY
            movement_count += 1
        if self.is_moving_right:
            movement_y += PERSON_MOVEMENT_VELOCITY
            movement_count += 1
        if self.is_moving_left:
            movement_y -= PERSON_MOVEMENT_VELOCITY
            movement_count += 1
        if movement_x != 0 or movement_y != 0:
            self.move(Vector2d(movement_x / movement_count, movement_y / movement_count))

    def cast(self):
        self.__fov.cast(self._vector2d)

    def move(self, movement: Vector2d):
        self.__last_pos = self._vector2d.copy()
        self._vector2d = ((self._vector2d ** -self.__fov.ang) + movement) ** self.__fov.ang

    def turn(self, angle: float):
        self.__fov.rot(angle)
