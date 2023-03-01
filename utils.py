import numpy as np
import matplotlib.pyplot as plt
def line_segment_intersection(line1, line2):
    x1, y1 = line1[0]
    x2, y2 = line1[1]
    x3, y3 = line2[0]
    x4, y4 = line2[1]

    # Calculate the denominator of the two linear equations
    denominator = (y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1)

    # If the denominator is zero, the lines are parallel
    if denominator == 0:
        return None

    # Calculate the numerators of the two linear equations
    ua = (x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)
    ub = (x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)

    # Calculate the values of u for the intersection point
    ua /= denominator
    ub /= denominator

    # If both values of u are between 0 and 1, the intersection point is inside both line segments
    if 0 <= ua <= 1 and 0 <= ub <= 1:
        # Calculate the intersection point
        x = x1 + ua * (x2 - x1)
        y = y1 + ua * (y2 - y1)
        return (x, y)

    # If the values of u are outside the range [0,1], the intersection point is outside one or both line segments
    return None

def ridges(sorted_polygon):
    return np.stack((sorted_polygon, np.roll(sorted_polygon, 1, axis = 0)), axis = 1)

def point_in_poly(point, sorted_polygon):
    x, y = point
    n = len(sorted_polygon)
    inside = False
    p1x, p1y = sorted_polygon[0]

    for i in range(1, n + 1):
        p2x, p2y = sorted_polygon[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xints = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xints:
                        inside = not inside
        p1x, p1y = p2x, p2y

    return inside


def polygon_intersection(sorted_polygon0, sorted_polygon1):

    """
    Calculates intersection of two polygons, returns intersection polygon or None. Works well only for convex polygons.
    """
    new_vertices = np.empty((0,2))
    # find all intersection between each ridge of both polygons and them to new_vericies
    for ridge0 in ridges(sorted_polygon0):
        for ridge1 in ridges(sorted_polygon1): 
            intersection = line_segment_intersection(ridge0, ridge1)
            if (intersection is not None):
                new_vertices = np.vstack((new_vertices, intersection))
    # find vertices of polygon0 that are inside polygon1 and them to new_vericies
    for vertice in sorted_polygon0:
        if point_in_poly(vertice, sorted_polygon1):
            new_vertices = np.vstack((new_vertices, vertice))

    # find vertices of polygon1 that are inside polygon0 and them to new_vericies
    for vertice in sorted_polygon1:
        if point_in_poly(vertice, sorted_polygon0):
            new_vertices = np.vstack((new_vertices, vertice))

    if new_vertices.size == 0:
        return None
    theta = np.angle((new_vertices[:,1]-np.average(new_vertices[:,1]))+ 
                     1j*(new_vertices[:,0]-np.average(new_vertices[:,0])))
    idx = np.argsort(theta)
    sorted_intersection = new_vertices[idx]
    return sorted_intersection


if __name__ == "__main__":


    # generate random sorted polygons
    n = np.random.randint(low = 3, high = 8)
    p0 = np.random.rand(n,2)*3-1
    theta = np.angle((p0[:,1]-np.average(p0[:,1]))+ 1j*(p0[:,0]-np.average(p0[:,0])))
    idx = np.argsort(theta)
    p0 = p0[idx]

    m = np.random.randint(low = 3, high = 8)
    p1 = np.random.rand(m,2)*3-1
    theta = np.angle((p1[:,1]-np.average(p1[:,1]))+ 1j*(p1[:,0]-np.average(p1[:,0])))
    idx = np.argsort(theta)
    p1 = p1[idx]

    intersectionp0p1 = polygon_intersection(p0, p1)


    for ridge in ridges(p0):
        plt.plot(ridge[:,0], ridge[:,1], color = 'C0')

    for ridge in ridges(p1):
        plt.plot(ridge[:,0], ridge[:,1], color = 'C1')

    if intersectionp0p1 is not None:
        for ridge in ridges(intersectionp0p1):
            plt.plot(ridge[:,0], ridge[:,1], color = 'C3')

    plt.show()
