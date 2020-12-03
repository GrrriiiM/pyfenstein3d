from pyfenstein3d.item import Item

class Wall(Item):
    def __init__(self, x: float, y: float, sprite_id: str):
        super().__init__(x, y, sprite_id, True)