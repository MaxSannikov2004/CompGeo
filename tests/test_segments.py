import random
from . import ref

def test_segments_intersect_from_statement(student):
    f = student.segments_intersect
    cases = [
        ((0,0),(2,0),(1,-1),(1,1), True),
        ((0,0),(2,0),(3,-1),(3,1), False),
        ((0,0),(2,0),(2,0),(3,0), True),   # касание концом
        ((0,0),(3,0),(1,0),(2,0), True),   # коллинеарное перекрытие
    ]
    for A,B,C,D,ans in cases:
        assert f(A,B,C,D) == ans

def test_segments_intersect_more_cases(student):
    f = student.segments_intersect
    # крест
    assert f((0,0),(2,2),(0,2),(2,0)) is True
    # T-образное
    assert f((0,0),(4,0),(2,-1),(2,1)) is True
    # параллельные раздельные
    assert f((0,0),(2,0),(0,1),(2,1)) is False
    # коллинеарные, но раздельные
    assert f((0,0),(1,0),(2,0),(3,0)) is False
    # вырожденный: точка-отрезок
    assert f((0,0),(0,0),(-1,-1),(1,1)) is True  # точка лежит на втором
    assert f((10,10),(10,10),(-1,-1),(1,1)) is False

def test_segments_intersect_random_integer(student):
    f = student.segments_intersect
    rng = random.Random(2)
    for _ in range(500):
        A = (rng.randint(-10,10), rng.randint(-10,10))
        B = (rng.randint(-10,10), rng.randint(-10,10))
        C = (rng.randint(-10,10), rng.randint(-10,10))
        D = (rng.randint(-10,10), rng.randint(-10,10))
        exp = ref.segments_intersect(A,B,C,D)
        got = f(A,B,C,D)
        assert got == exp
