from .person import Person
from .field_of_view import FieldOfView


class Player(Person):
    def __init__(self, vector_x: float, vector_y: float, type_id: int, fov: FieldOfView, player_id: str):
        super().__init__(vector_x, vector_y, type_id, fov)
        self.__id = player_id
