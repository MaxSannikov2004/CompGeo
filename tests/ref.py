import math

EPS = 1e-9

def orient(A, B, C, eps=EPS):
    ax, ay = A
    bx, by = B
    cx, cy = C
    cross = (bx-ax)*(cy-ay) - (by-ay)*(cx-ax)
    if abs(cross) <= eps:
        return 0
    return 1 if cross > 0 else -1

def on_segment(A, B, P, eps=EPS):
    if orient(A, B, P, eps) != 0:
        return False
    ax, ay = A; bx, by = B; px, py = P
    return (min(ax, bx) - eps <= px <= max(ax, bx) + eps and
            min(ay, by) - eps <= py <= max(ay, by) + eps)

def segments_intersect(A, B, C, D, eps=EPS):
    o1 = orient(A, B, C, eps)
    o2 = orient(A, B, D, eps)
    o3 = orient(C, D, A, eps)
    o4 = orient(C, D, B, eps)

    if o1*o2 < 0 and o3*o4 < 0:
        return True
    if o1 == 0 and on_segment(A, B, C, eps): return True
    if o2 == 0 and on_segment(A, B, D, eps): return True
    if o3 == 0 and on_segment(C, D, A, eps): return True
    if o4 == 0 and on_segment(C, D, B, eps): return True
    return False

def polygon_area(poly):
    s = 0.0
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i+1) % n]
        s += x1*y2 - y1*x2
    return 0.5*s

def point_in_polygon(Q, poly, eps=EPS):
    x, y = Q
    inside = False
    n = len(poly)
    for i in range(n):
        A = poly[i]
        B = poly[(i+1) % n]
        if on_segment(A, B, Q, eps):
            return True

        x1, y1 = A
        x2, y2 = B
        if y1 > y2:
            x1, y1, x2, y2 = x2, y2, x1, y1

        if y1 <= y < y2 and abs(y2 - y1) > eps:
            x_int = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
            if x_int > x:
                inside = not inside
    return inside
