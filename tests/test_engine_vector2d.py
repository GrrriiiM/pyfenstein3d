import math
from engine import Vector2d

def test_init():
    vector = Vector2d(10, 0)
    assert vector.x == 10
    assert vector.y == 0
    assert round(vector.ang, 3) == 0
    assert round(vector.mag, 3) == 10
    vector = Vector2d(10, 10)
    assert vector.x == 10
    assert vector.y == 10
    assert round(vector.ang, 3) == round(math.pi / 4, 3)
    assert round(vector.mag, 3) == 14.142

def test_add():
    vec1 = Vector2d(1, 2)
    vec2 = Vector2d(3, 4)
    vec3 = vec1 + vec2
    assert vec3.x == 4
    assert vec3.y == 6

def test_sub():
    vec1 = Vector2d(1, 2)
    vec2 = Vector2d(3, 5)
    vec3 = vec1 - vec2
    assert vec3.x == -2
    assert vec3.y == -3

def test_mult():
    vec = Vector2d(4, 3)
    vec = vec * 2
    assert vec.x == 8
    assert vec.y == 6

def test_div():
    vec = Vector2d(4, 3)
    vec = vec / 2
    assert vec.x == 2
    assert vec.y == 1.5

def test_floordiv():
    vec = Vector2d(5, 7)
    vec = vec // 2
    assert vec.x == 2
    assert vec.y == 3

def test_rot():
    vec = Vector2d(4, 3)
    vec = vec ** (math.pi / 2)
    assert round(vec.x, 0) == -3
    assert round(vec.y, 0) == 4

def test_copy():
    vec = Vector2d(4, 3)
    vec1 = vec.copy()
    assert vec != vec1
    assert vec.x == vec1.x
    assert vec.y == vec1.y

def test_norm():
    vec = Vector2d(4, 3)
    vec = vec % 1
    assert vec.mag == 1
