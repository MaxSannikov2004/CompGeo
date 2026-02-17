import random
from . import ref

def test_polygon_area_square_signed(student):
    area = student.polygon_area
    square_ccw = [(0,0),(1,0),(1,1),(0,1)]
    square_cw  = [(0,0),(0,1),(1,1),(1,0)]
    assert abs(area(square_ccw) - 1.0) < 1e-9
    assert abs(area(square_cw) + 1.0) < 1e-9

def test_polygon_area_translation_invariant(student):
    area = student.polygon_area
    poly = [(0,0),(3,0),(3,2),(0,2)]
    a0 = area(poly)
    shift = (10, -7)
    poly2 = [(x+shift[0], y+shift[1]) for x,y in poly]
    assert abs(area(poly2) - a0) < 1e-9

def test_point_in_polygon_square(student):
    pip = student.point_in_polygon
    square = [(0,0),(2,0),(2,2),(0,2)]
    assert pip((1,1), square) is True
    assert pip((3,3), square) is False
    assert pip((0,1), square) is True   # граница
    assert pip((2,2), square) is True   # вершина

def test_point_in_polygon_concave(student):
    pip = student.point_in_polygon
    # "стрелка" (вогнутый)
    poly = [(0,0),(4,0),(4,4),(2,2),(0,4)]
    assert pip((1,1), poly) is True
    assert pip((3,3), poly) is True
    assert pip((2.5,2.0), poly) is True
    assert pip((2,3), poly) is False  # в "вырезе"

def test_point_in_polygon_random_against_reference(student):
    pip = student.point_in_polygon
    rng = random.Random(3)
    # простой выпуклый многоугольник (прямоугольник), чтобы избежать сложных граничных случаев
    poly = [(-5,-2),(6,-2),(6,7),(-5,7)]
    for _ in range(500):
        Q = (rng.uniform(-10,10), rng.uniform(-10,10))
        exp = ref.point_in_polygon(Q, poly)
        got = pip(Q, poly)
        assert got == exp
