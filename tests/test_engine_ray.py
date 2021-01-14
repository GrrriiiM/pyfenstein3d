import math
from pytest import approx
from engine import Ray
from engine import Vector2d
from engine import Wall
from engine import ItemGrid

def test_init():
    v2d = Vector2d(10.2, 5.3)
    ray = Ray(math.pi * 0.25)
    assert ray.ang == approx(math.pi * 0.25)
    assert ray.dir_x == 1
    assert ray.dir_y == 1
    assert ray.delta_dist_x == approx(1.4142, 0.0001)
    assert ray.delta_dist_y == approx(1.4142, 0.0001)
    assert ray.get_dist_x(v2d) == approx(1.1314, 0.0001)
    assert ray.get_dist_y(v2d) == approx(0.9899, 0.0001)
    ray.rot(math.pi * 0.5)
    assert ray.ang == approx(math.pi * 0.75)
    assert ray.dir_x == -1
    assert ray.dir_y == 1
    assert ray.delta_dist_x == approx(1.4142, 0.0001)
    assert ray.delta_dist_y == approx(1.4142, 0.0001)
    assert ray.get_dist_x(v2d) == approx(0.28284, 0.0001)
    assert ray.get_dist_y(v2d) == approx(0.9899, 0.0001)
    ray.rot(math.pi * 0.5)
    assert ray.ang == approx(math.pi * 1.25)
    assert ray.dir_x == -1
    assert ray.dir_y == -1
    assert ray.delta_dist_x == approx(1.4142, 0.0001)
    assert ray.delta_dist_y == approx(1.4142, 0.0001)
    assert ray.get_dist_x(v2d) == approx(0.28284, 0.0001)
    assert ray.get_dist_y(v2d) == approx(0.42426, 0.0001)
    ray.rot(math.pi * 0.5)
    assert ray.ang == approx(math.pi * 1.75)
    assert ray.dir_x == 1
    assert ray.dir_y == -1
    assert ray.delta_dist_x == approx(1.4142, 0.0001)
    assert ray.delta_dist_y == approx(1.4142, 0.0001)
    assert ray.get_dist_x(v2d) == approx(1.1314, 0.0001)
    assert ray.get_dist_y(v2d) == approx(0.42426, 0.0001)

def test_cast_wall_1():
    pos = Vector2d(1.3, 2.2)
    ray = Ray(math.pi / 6)

    wall1 = Wall(2, 3, 10)
    ray.cast_wall(pos, ItemGrid([wall1]))
    assert ray.type_id == wall1.type_id
    assert not ray.is_vertical
    assert not ray.is_inverted
    assert ray.collided_vector2d.x == approx(2.69, abs=0.01)
    assert ray.collided_vector2d.y == approx(3, abs=0.01)
    assert ray.dist_adjusted == approx(1.39, abs=0.01)
    assert ray.offset == approx(0.69, abs=0.01)

    wall2 = Wall(7, 6, 20)
    ray.cast_wall(pos, ItemGrid([wall2]))
    assert ray.type_id == wall2.type_id
    assert not ray.is_vertical
    assert not ray.is_inverted
    assert ray.collided_vector2d.x == approx(7.88, abs=0.01)
    assert ray.collided_vector2d.y == approx(6, abs=0.01)
    assert ray.dist_adjusted == approx(6.58, abs=0.01)
    assert ray.offset == approx(0.88, abs=0.01)

def test_cast_wall_2():
    pos = Vector2d(4.4, 2.4)
    ray = Ray(math.pi + math.pi / 6)

    wall = Wall(10, 10, 10)
    wall1 = Wall(3, 1, 10)

    ray.cast_wall(pos, ItemGrid([wall1, wall]))
    assert ray.type_id == wall1.type_id
    assert not ray.is_vertical
    assert ray.is_inverted
    assert ray.collided_vector2d.x == approx(3.71, abs=0.01)
    assert ray.collided_vector2d.y == approx(2, abs=0.01)
    assert ray.dist_adjusted == approx(0.69, abs=0.01)
    assert ray.offset == approx(0.71, abs=0.01)

    wall2 = Wall(1, 0, 10)
    ray.cast_wall(pos, ItemGrid([wall2, wall]))
    assert ray.type_id == wall2.type_id
    assert not ray.is_vertical
    assert ray.is_inverted
    assert ray.collided_vector2d.x == approx(1.98, abs=0.01)
    assert ray.collided_vector2d.y == approx(1, abs=0.01)
    assert ray.dist_adjusted == approx(2.42, abs=0.01)
    assert ray.offset == approx(0.98, abs=0.01)

def test_cast_wall_3():
    pos = Vector2d(1.4, 2.5)
    ray = Ray(math.pi / 6)

    wall = Wall(10, 10, 10)
    wall1 = Wall(2, 2, 10)

    ray.cast_wall(pos, ItemGrid([wall1, wall]))
    assert ray.type_id == wall1.type_id
    assert ray.is_vertical
    assert not ray.is_inverted
    assert ray.collided_vector2d.x == approx(2, abs=0.01)
    assert ray.collided_vector2d.y == approx(2.85, abs=0.01)
    assert ray.dist_adjusted == approx(0.6, abs=0.01)
    assert ray.offset == approx(0.85, abs=0.01)
