"""contem classe Vector2d"""

import math

class Vector2d():
    """permite realizar calculos vetoriais"""
    def __init__(self, x: float = 0, y: float = 0):
        self.set_x_y(x, y)

    def get_x(self) -> float:
        """obtem x"""
        return self.__x

    def set_x(self, v_x):
        """atribui x"""
        self.set_x_y(v_x, self.__y)
    x: float = property(get_x, set_x)

    def get_y(self) -> float:
        """obtem y"""
        return self.__y

    def set_y(self, v_y: float):
        """atribui y"""
        self.set_x_y(self.__x, v_y)
    y: float = property(get_y, set_y)

    def get_mag(self) -> float:
        """obtem magnitude"""
        return self.__mag
    mag: float = property(get_mag)

    def get_ang(self) -> float:
        """obtem angulo"""
        return self.__ang
    ang = property(get_ang)

    def set_x_y(self, vector_x: float, vector_y: float):
        """atribui x e y"""
        self.__x = vector_x
        self.__y = vector_y
        self.__ang = math.atan2(vector_x, vector_y)
        self.__mag = math.sqrt(math.pow(vector_x, 2) + math.pow(vector_y, 2))

    def copy(self):
        """cria copia"""
        return Vector2d(self.x, self.y)

    def norm(self):
        """normaliza vetor"""
        mag = self.mag
        if mag == 0:
            return self
        self.set_x_y(self.__x / mag, self.__y / mag)
        return self

    def rot(self, rad: float):
        """aplica rotacao"""
        cos = math.cos(rad)
        sin = math.sin(rad)
        v_x = self.x
        v_y = self.y
        self.set_x_y(v_x * cos - v_y * sin, v_x * sin + v_y * cos)
        return self

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
