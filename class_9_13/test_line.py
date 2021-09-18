from line import *

def test_line_cal():
    slope, inter = line_cal(1, 1, 2, 2)
    assert slope == 1
    assert inter == 0

def test_ycoor_cal():
    y = ycoor_cal(1, 0, 5)
    assert y == 5
