import math
import random
import numpy as np
from . import ref

def test_orient_basic(student):
    o = student.orient
    assert o((0,0),(1,0),(0,1)) == 1
    assert o((0,0),(1,0),(0,-1)) == -1
    assert o((0,0),(1,0),(2,0)) == 0

def test_orient_returns_only_signs(student):
    # В этом задании orient — именно предикат знака.
    for pts in [
        ((0,0),(2,0),(1,1)),
        ((0,0),(2,0),(1,-1)),
        ((0,0),(2,0),(1,0)),
    ]:
        v = student.orient(*pts)
        assert v in (-1, 0, 1)

def test_orient_random_integer(student):
    o = student.orient
    rng = random.Random(0)
    for _ in range(500):
        A = (rng.randint(-10,10), rng.randint(-10,10))
        B = (rng.randint(-10,10), rng.randint(-10,10))
        C = (rng.randint(-10,10), rng.randint(-10,10))
        exp = ref.orient(A,B,C)
        got = o(A,B,C)
        assert got == exp

def test_dist_point_line_known(student):
    d = student.dist_point_line
    assert abs(d((3,4), 1, 0, 0) - 3.0) < 1e-9   # x = 0
    assert abs(d((0,0), 0, 1, -2) - 2.0) < 1e-9  # y = 2

def test_dist_point_line_scale_invariant(student):
    d = student.dist_point_line
    P = (1.25, -3.5)
    a,b,c = 2.0, -1.0, 0.75
    v1 = d(P, a,b,c)
    v2 = d(P, 10*a, 10*b, 10*c)
    assert abs(v1 - v2) < 1e-9

def test_dist_point_line_invalid(student):
    d = student.dist_point_line
    try:
        d((0,0), 0, 0, 1)
        assert False, "ожидался ValueError при a=b=0"
    except ValueError:
        pass

def test_on_segment_simple(student):
    on = student.on_segment
    assert on((0,0),(2,0),(0,0))  # конец
    assert on((0,0),(2,0),(2,0))  # конец
    assert on((0,0),(2,0),(1,0))  # середина
    assert not on((0,0),(2,0),(3,0))  # за пределами
    assert not on((0,0),(2,0),(1,1))  # не коллинеарна

def test_on_segment_random_parametric(student):
    on = student.on_segment
    rng = random.Random(1)
    for _ in range(200):
        A = (rng.randint(-20,20), rng.randint(-20,20))
        B = (rng.randint(-20,20), rng.randint(-20,20))
        t = rng.random()
        P = (A[0] + t*(B[0]-A[0]), A[1] + t*(B[1]-A[1]))
        assert on(A,B,P)

def test_on_segment_collinear_outside(student):
    on = student.on_segment
    A = (0,0); B=(2,2)
    assert not on(A,B,(-1,-1))
    assert not on(A,B,(3,3))
