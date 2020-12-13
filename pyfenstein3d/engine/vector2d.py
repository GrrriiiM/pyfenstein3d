"""contem classe Vector2d"""

import math

class Vector2d():
    """permite realizar calculos vetoriais"""
    def __init__(self, x: float = 0, y: float = 0):
        self.__x = x
        self.__y = y
        self.__ang = (math.atan2(self.__y, self.__x) + math.pi * 2) % (math.pi * 2)
        self.__mag = math.sqrt(math.pow(self.__x, 2) + math.pow(self.__y, 2))

    def get_x(self) -> float:
        """obtem x"""
        return self.__x
    x: float = property(get_x)

    def get_y(self) -> float:
        """obtem y"""
        return self.__y
    y: float = property(get_y)

    def get_mag(self) -> float:
        """obtem magnitude"""
        return self.__mag
    mag: float = property(get_mag)

    def get_ang(self) -> float:
        """obtem angulo"""
        return self.__ang
    ang = property(get_ang)

    def copy(self):
        """cria copia"""
        return Vector2d(self.x, self.y)

    def __add__(self, other):
        return Vector2d(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2d(self.x - other.x, self.y - other.y)

    def __mul__(self, other: float):
        return Vector2d(self.x * other, self.y * other)

    def __truediv__(self, other: float):
        return Vector2d(self.x / other, self.y / other)

    def __floordiv__(self, other: float):
        return Vector2d(self.x // other, self.y // other)

    def __pow__(self, other: float):
        cos = math.cos(other)
        sin = math.sin(other)
        v_x = self.x
        v_y = self.y
        return Vector2d(v_x * cos - v_y * sin, v_x * sin + v_y * cos)

    def __mod__(self, other: float):
        mag = self.mag
        if mag == 0:
            return self
        return Vector2d((self.__x / mag) * other, (self.__y / mag) * other)

    @staticmethod
    def create_with_ang(rad: float):
        return Vector2d(math.cos(rad), math.sin(rad))
