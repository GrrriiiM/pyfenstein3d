from .item import Item

class ItemAmmo(Item):
    def touch(self, player, grid):
        player.add_ammo(4)
        grid.remove_block(self.x, self.y)
