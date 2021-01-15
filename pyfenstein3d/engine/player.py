import uuid
from .person import Person
from .field_of_view import FieldOfView
from .vector2d import Vector2d
from .item_grid import ItemGrid
from .weapon import WeaponPistol


class Player(Person):
    def __init__(self, vector_x: float, vector_y: float, type_id: int, fov: FieldOfView, player_id: str):
        super().__init__(vector_x, vector_y, type_id, fov)
        self.__player_id = player_id
        self.__weapon = WeaponPistol()

    @property
    def player_id(self):
        return self.__player_id

    def update(self, delta_time: float, grid: ItemGrid):
        super().update(delta_time, grid)
        self.__weapon.update(delta_time, grid)


    @staticmethod
    def create(vector_x: float, vector_y: float, type_id: int):
        return Player(vector_x, vector_y, type_id, FieldOfView(0), "123")#uuid.uuid4())

