def manhattan_distance(p1, p2):
    """
        p1, p2 : tuples -> (x,y)
        Distance between two points.
        return Int
    """
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)
