import numpy as np
import shapely as sp


def angle_between_vectors(
    v1: np.ndarray, v2: np.ndarray
):  # TODO: duplicated code for findinf angles .. -> really should be in utils4plans
    # TODO: can geom library handle this?
    dot_product = np.dot(v1, v2)
    magnitude_v1 = np.linalg.norm(v1)
    magnitude_v2 = np.linalg.norm(v2)

    # Handle cases where one or both vectors are zero vectors to avoid division by zero
    if magnitude_v1 == 0 or magnitude_v2 == 0:
        return 0.0  # Or raise an error, depending on desired behavior

    cosine_theta = dot_product / (magnitude_v1 * magnitude_v2)

    # Ensure cosine_theta is within [-1, 1] to prevent issues with arccos due to floating point inaccuracies
    cosine_theta = np.clip(cosine_theta, -1.0, 1.0)

    angle_radians = np.arccos(cosine_theta)
    return angle_radians


def get_line_between_line_and_point(line: sp.LineString, pt: sp.Point):
    dist_along = line.project(pt)
    ptb = line.line_interpolate_point(dist_along)
    return sp.LineString([pt, ptb])


def translate_line_to_origin(line: sp.LineString, pt: sp.Point):
    assert pt.touches(line)
    return sp.affinity.translate(line, xoff=-1 * pt.x, yoff=-1 * pt.y)


def get_rotation_angle(poly: sp.Polygon):
    # Construct a line on the boundary of the polygon
    # TODO: put this under test!
    coords = list(poly.exterior.normalize().coords)
    # TODO: put this in a NamedTuple
    right_line = sp.LineString(coords[2:4])
    centroid = poly.centroid
    assert right_line.centroid.x > centroid.x

    # Create a vector pointing from the polygon's centroid to the constructed line
    vector_line = get_line_between_line_and_point(right_line, centroid)
    # Translate the vector to the origin to that can find the angle between the translated vector and e1 (basis vector along the x-axis)
    translated_line = translate_line_to_origin(vector_line, centroid)
    non_zero_pt = list(translated_line.coords)[1]
    v1 = np.array(non_zero_pt)
    e0 = np.array([1, 0])

    return angle_between_vectors(e0, v1)


def rotate_multipolygon(multpol: sp.MultiPolygon):
    bound_rect: sp.Polygon = multpol.minimum_rotated_rectangle.normalize()  # type: ignore
    angle = get_rotation_angle(bound_rect)
    rotated_multpol = sp.affinity.rotate(multpol, angle, use_radians=True)
    return angle, rotated_multpol
