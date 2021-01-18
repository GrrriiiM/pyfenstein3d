from .item import Item

class ItemScore(Item):
    def touch(self, player):
        if self.type_id == 87:
            player.add_score(100)
        elif self.type_id == 88:
            player.add_score(400)
        elif self.type_id == 89:
            player.add_score(800)
