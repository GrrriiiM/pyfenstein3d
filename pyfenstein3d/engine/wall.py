from .block import Block

class Wall(Block):
    def __init__(self, x: float, y: float, type_id: int):
        super().__init__(x, y, type_id, True)
