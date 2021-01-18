import math
from .block import Block
from .vector2d import Vector2d
from .field_of_view import FieldOfView
from .config import PERSON_TURN_VELOCITY
from .config import PERSON_MOVEMENT_VELOCITY
from .item_grid import ItemGrid
from .weapon import WeaponPistol

class Person(Block):
    def __init__(self, vector_x: float, vector_y: float, type_id: int, fov: FieldOfView):
        super().__init__(vector_x, vector_y, type_id, True, True)
        self.__fov = fov
        self.__last_pos = self._vector2d.copy()
        self.is_turning_left = False
        self.is_turning_right = False
        self.is_moving_front = False
        self.is_moving_back = False
        self.is_moving_left = False
        self.is_moving_right = False
        self.is_interacting = False
        self._weapon = WeaponPistol()

    @property
    def fov(self):
        return self.__fov

    @property
    def fov_ang(self):
        return self.__fov.ang

    @property
    def weapon(self):
        return self._weapon;

    def update(self, delta_time: float, grid: ItemGrid):
        if self.is_turning_left:
            self.turn(-PERSON_TURN_VELOCITY * delta_time)
        if self.is_turning_right:
            self.turn(PERSON_TURN_VELOCITY * delta_time)
        movement_x = 0
        movement_y = 0
        movement_count = 0
        if self.is_moving_front:
            movement_x += PERSON_MOVEMENT_VELOCITY * delta_time
            movement_count += 1
        if self.is_moving_back:
            movement_x -= PERSON_MOVEMENT_VELOCITY * delta_time
            movement_count += 1
        if self.is_moving_right:
            movement_y += PERSON_MOVEMENT_VELOCITY * delta_time
            movement_count += 1
        if self.is_moving_left:
            movement_y -= PERSON_MOVEMENT_VELOCITY * delta_time
            movement_count += 1
        if movement_x != 0 or movement_y != 0:
            self.move(Vector2d(movement_x / movement_count, movement_y / movement_count))
        if self.is_interacting:
            self.interact(grid)
        self._weapon.update(delta_time, self, grid)

    def can_shoot(self):
        return True

    def shoot(self):
        pass

    def adjust_collision(self, grid: ItemGrid):
        diff_pos = self._vector2d - self.__last_pos
        item = grid.get_block(math.floor(self._vector2d.x + math.copysign(0.5, diff_pos.x)), math.floor(self.__last_pos.y))
        if item is not None and item.is_solid:
            if diff_pos.x > 0:
                self._vector2d = Vector2d(item.block_x - 0.5, self._vector2d.y)
            elif diff_pos.x < 0:
                self._vector2d = Vector2d(item.block_x + 1.5, self._vector2d.y)

        item = grid.get_block(math.floor(self.__last_pos.x), math.floor(self._vector2d.y + math.copysign(0.5, diff_pos.y)))
        if item is not None and item.is_solid:
            if diff_pos.y > 0:
                self._vector2d = Vector2d(self._vector2d.x, item.block_y - 0.5)
            elif diff_pos.y < 0:
                self._vector2d = Vector2d(self._vector2d.x, item.block_y + 1.5)

    def cast(self, grid: ItemGrid):
        self.__fov.cast(self._vector2d, grid)

    def move(self, movement: Vector2d):
        self.__last_pos = self._vector2d.copy()
        self._vector2d = ((self._vector2d ** -self.__fov.ang) + movement) ** self.__fov.ang

    def turn(self, angle: float):
        self.__fov.rot(angle)

    def interact(self, grid: ItemGrid):
        view_dir = (Vector2d.create_with_ang(self.fov.ang) % 0.75) + self._vector2d
        block = grid.get_block(view_dir.x, view_dir.y)
        if block is not None:
            block.interacted()
