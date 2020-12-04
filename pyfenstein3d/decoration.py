from pyfenstein3d.item import Item

class Decoration(Item):
    def __init__(self, vector_x: float, vector_y: float, type_id: str, is_solid: bool):
        super().__init__(vector_x, vector_y, type_id, is_solid)
