class Weapon():
    def __init__(self, type_id:int):
        self.__type_id = type_id

class WeaponPistol(Weapon):
    def __init__(self):
        super().__init__(251)
