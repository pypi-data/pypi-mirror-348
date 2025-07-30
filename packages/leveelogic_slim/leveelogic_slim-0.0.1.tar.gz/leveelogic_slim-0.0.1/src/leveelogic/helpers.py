from typing import List, Tuple
from shapely.geometry import (
    LineString,
    MultiPoint,
    GeometryCollection,
    MultiLineString,
    Point,
    Polygon,
)
from shapely import get_coordinates
from pathlib import Path


def case_insensitive_glob(filepath: str, fileextension: str) -> List[Path]:
    """Find files in given path with given file extension (case insensitive)

    Arguments:
        filepath (str): path to files
        fileextension (str): file extension to use as a filter (example .gef or .csv)

    Returns:
        List(str): list of files
    """
    p = Path(filepath)
    result = []
    for filename in p.glob("**/*"):
        if str(filename.suffix).lower() == fileextension.lower():
            result.append(filename.absolute())
    return result


def is_point_in_or_on_polygon(point: tuple, polygon_coords: list) -> bool:
    """
    Check if a point is inside a polygon or on its boundary.

    Args:
        point (tuple): A tuple representing the point (x, y).
        polygon_coords (list): A list of tuples representing the polygon vertices [(x1, y1), (x2, y2), ...].

    Returns:
        bool: True if the point is inside or on the boundary of the polygon, False otherwise.
    """
    shapely_point = Point(point)
    shapely_polygon = Polygon(polygon_coords)

    return shapely_polygon.contains(shapely_point) or shapely_polygon.touches(
        shapely_point
    )


def polyline_polyline_intersections(
    points_line1: List[Tuple[float, float]],
    points_line2: List[Tuple[float, float]],
) -> List[Tuple[float, float]]:
    """Find the intersection points of two polylines."""
    result = []

    ls1 = LineString(points_line1)
    ls2 = LineString(points_line2)
    intersections = ls1.intersection(ls2)

    if intersections.is_empty:
        return []
    elif type(intersections) == MultiPoint:
        result = [(g.x, g.y) for g in intersections.geoms]
    elif type(intersections) == Point:
        x, y = intersections.coords.xy
        result = [(x[0], y[0])]
    elif type(intersections) == LineString:
        result += [(p[0], p[1]) for p in get_coordinates(intersections).tolist()]
    elif type(intersections) == GeometryCollection:
        geoms = [g for g in intersections.geoms if type(g) != Point]
        result += [(p[0], p[1]) for p in get_coordinates(geoms).tolist()]
        for p in [g for g in intersections.geoms if type(g) == Point]:
            x, y = p.coords.xy
            result.append((x[0], y[0]))
    elif type(intersections) == MultiLineString:
        geoms = [g for g in intersections.geoms if type(g) != Point]
        if len(geoms) >= 2:
            x1, z1 = geoms[0].coords.xy
            x2, z2 = geoms[1].coords.xy

            if x1 == x2:  # vertical
                x = x1.tolist()[0]
                zs = z1.tolist() + z2.tolist()
                result.append((x, min(zs)))
                result.append((x, max(zs)))
            elif z1 == z2:  # horizontal
                z = z1.tolist()[0]
                xs = x1.tolist() + x2.tolist()
                result.append((min(xs), z))
                result.append((max(xs), z))
            else:
                raise ValueError(
                    f"Unimplemented intersection type '{type(intersections)}' that is not a horizontal or vertical line or consists of more than 2 lines"
                )
        else:
            raise ValueError(
                f"Unimplemented intersection type '{type(intersections)}' with varying x or z coordinates"
            )
    else:
        raise ValueError(
            f"Unimplemented intersection type '{type(intersections)}' {points_line1}"
        )

    # do not include points that are on line1 or line2
    # final_result = [float(p) for p in result if not p in points_line1 or p in points_line2]

    # if len(final_result) == 0:
    #    return []

    return sorted(result, key=lambda x: x[0])
