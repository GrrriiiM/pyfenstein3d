from .item import Item

class ItemAmmo(Item):
    def touch(self, player):
        player.add_ammo(4)
