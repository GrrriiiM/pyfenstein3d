import uuid
from .person import Person
from .field_of_view import FieldOfView
from .vector2d import Vector2d
from .item_grid import ItemGrid


class Player(Person):
    def __init__(self, vector_x: float, vector_y: float, type_id: int, fov: FieldOfView, player_id: str):
        super().__init__(vector_x, vector_y, type_id, fov)
        self.player_id = player_id


    @staticmethod
    def create(vector_x: float, vector_y: float, type_id: int):
        return Player(vector_x, vector_y, type_id, FieldOfView(0), "123")#uuid.uuid4())
