import numpy as np

def normalize_array(array, lower_bound=0, upper_bound=1):
    array_min = np.min(array)
    array_max = np.max(array)
    normalized_array = (array - array_min) / (array_max - array_min)
    normalized_array = lower_bound + normalized_array * (upper_bound - lower_bound)
    return normalized_array.astype('float32')

def bresenham(start_coords, end_coords):
    sx, sy = start_coords
    ex, ey = end_coords
    dx = abs(ex - sx)
    dy = abs(ey - sy)
    is_steep = dy > dx

    if is_steep:
        sx, sy = sy, sx
        ex, ey = ey, ex

    swap = False
    if sx > ex:
        sx, ex = ex, sx
        sy, ey = ey, sy
        swap = True

    dx = ex - sx
    dy = abs(ey - sy)
    err = dx / 2
    ystep = 1 if sy < ey else -1

    y = sy
    points = []
    for x in range(sx, ex + 1):
        coord = (y, x) if is_steep else (x, y)
        points.append(coord)
        err -= dy
        if err < 0:
            y += ystep
            err += dx

    if swap:
        points.reverse()

    return np.array(points).T