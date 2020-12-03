from pyfenstein3d.item import Item

class Decoration(Item):
    def __init__(self, x: float, y: float, sprite_id: str, is_solid: bool):
        super().__init__(x, y, sprite_id, is_solid)