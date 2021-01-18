from .item import Item
from .player import Player
from .weapon import WeaponSubmachine
from .weapon import WeaponMinigun

class ItemWeapon(Item):
    def touch(self, player: Player):
        if self.type_id == 85:
            player.change_weapon(WeaponSubmachine)
        elif self.type_id == 86:
            player.change_weapon(WeaponMinigun)
