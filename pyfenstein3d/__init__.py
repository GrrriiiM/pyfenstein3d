from pyfenstein3d.vector2d import Vector2d
from pyfenstein3d.item import Item
from pyfenstein3d.decoration import Decoration
from pyfenstein3d.wall import Wall
from pyfenstein3d.map2d import Map2d

def create_vector2d(vector_x: float, vector_y: float):
    return Vector2d(vector_x, vector_y)

def create_item(vector_x: float, vector_y: float, type_id: str, is_solid: bool=False):
    return Item(vector_x, vector_y, type_id, is_solid)

def create_decoration(vector_x: float, vector_y: float, type_id: str, is_solid: bool=False):
    return Decoration(vector_x, vector_y, type_id, is_solid)

def create_wall(vector_x: float, vector_y: float, type_id: str):
    return Wall(vector_x, vector_y, type_id)

def create_map2d(items: []):
    return Map2d(items)

def create_map2d_with_file(file_path: str):
    return Map2d.create_with_file(file_path)

def create_map2d_with_pattern(pattern: str):
    return Map2d.create_with_pattern(pattern)
