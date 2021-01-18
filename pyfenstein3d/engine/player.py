import uuid
from .person import Person
from .field_of_view import FieldOfView
from .vector2d import Vector2d
from .item_grid import ItemGrid
from .weapon import Weapon
from .item import Item


class Player(Person):
    def __init__(self, vector_x: float, vector_y: float, type_id: int, fov: FieldOfView, player_id: str):
        super().__init__(vector_x, vector_y, type_id, fov)
        self.__player_id = player_id
        self.__health = 100
        self.__ammo = 10
        self.__score = 0

    @property
    def health(self):
        return self.__health

    @property
    def ammo(self):
        return self.__ammo

    @property
    def score(self):
        return self.__score

    @property
    def player_id(self):
        return self.__player_id

    def change_weapon(self, weapon):
        self._weapon = weapon

    def update(self, delta_time: float, grid: ItemGrid):
        super().update(delta_time, grid)
        block = grid.get_block(self.x, self.y)
        if isinstance(block, Item) :
            block.touch(self)


    @staticmethod
    def create(vector_x: float, vector_y: float, type_id: int):
        return Player(vector_x, vector_y, type_id, FieldOfView(0), "123")#uuid.uuid4())

