import uuid
from .person import Person
from .field_of_view import FieldOfView
from .vector2d import Vector2d
from .item_grid import ItemGrid
from .weapon import Weapon
from .weapon import WeaponKnife
from .weapon import WeaponPistol
from .item import Item


class Player(Person):
    def __init__(self, vector_x: float, vector_y: float, type_id: int, fov: FieldOfView, player_id: str):
        super().__init__(vector_x, vector_y, type_id, fov)
        self.__player_id = player_id
        self.__health = 100
        self.__ammo = 8
        self.__score = 0
        self.change_weapon(WeaponPistol)
        

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

    def shoot(self):
        self.__ammo -= 1
        self.__ammo = self.__ammo if self.__ammo >= 0 else 0
        if self.__ammo <= 0 and not isinstance(self._weapon, WeaponKnife):
            self._weapon = WeaponKnife()

    def change_weapon(self, weapon_type):
        self.__weapon_type = weapon_type
        if self.__ammo > 0:
            self._weapon = self.__weapon_type()

    def add_ammo(self, quantity):
        self.__ammo += quantity
        self.__ammo = self.__ammo if self.__ammo < 999 else 999
        if self.__ammo > 0:
            self._weapon = self.__weapon_type()

    def add_score(self, quantity):
        self.__score += quantity

    def update(self, delta_time: float, grid: ItemGrid):
        super().update(delta_time, grid)
        block = grid.get_block(self.x, self.y)
        if isinstance(block, Item) :
            block.touch(self)
            grid.remove_block(self.x, self.y)

    @staticmethod
    def create(vector_x: float, vector_y: float, type_id: int):
        return Player(vector_x, vector_y, type_id, FieldOfView(0), "123")#uuid.uuid4())
