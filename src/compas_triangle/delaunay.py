from typing import Annotated
from typing import Optional

from compas.geometry import centroid_points_xy
from compas.itertools import pairwise
from compas.plugins import plugin
from compas.tolerance import TOL
from triangle import triangulate

geo = TOL.geometric_key_xy


Point = Annotated[list[float], 3]
Polyline = list[Point]
Polygon = list[Point]
Segment = tuple[int, int]
Triangle = tuple[int, int, int]


def _to_vertices_segments_holes(
    boundary: list[Point],
    polylines: list[Polyline],
    polygons: list[Polygon],
) -> tuple[list[Point], list[Segment], list[Point]]:
    if geo(boundary[0]) != geo(boundary[-1]):
        boundary.append(boundary[0])

    gkey_xyz = {geo(point): point[:2] for point in boundary}

    if polylines:
        for polyline in polylines:
            gkey_xyz.update({geo(point): point[:2] for point in polyline})

    if polygons:
        for polygon in polygons:
            if geo(polygon[0]) != geo(polygon[-1]):
                polygon.append(polygon[0])

            gkey_xyz.update({geo(point): point[:2] for point in polygon})

    gkey_index = {gkey: index for index, gkey in enumerate(gkey_xyz)}

    vertices = list(gkey_xyz.values())
    segments = [(gkey_index[geo(a)], gkey_index[geo(b)]) for a, b in pairwise(boundary)]
    holes = []

    if polylines:
        for polyline in polylines:
            segments += [(gkey_index[geo(a)], gkey_index[geo(b)]) for a, b in pairwise(polyline)]

    if polygons:
        for polygon in polygons:
            segments += [(gkey_index[geo(a)], gkey_index[geo(b)]) for a, b in pairwise(polygon)]
            points = [vertices[gkey_index[geo(point)]] for point in polygon]
            centroid = centroid_points_xy(points)
            holes.append(centroid[:2])

    return vertices, segments, holes


@plugin(category="triangulation")
def delaunay_triangulation(points: list[Point]) -> tuple[list[Point], list[Triangle]]:
    """Construct a Delaunay triangulation of set of vertices.

    Parameters
    ----------
    points : list
        XY(Z) coordinates of the points to triangulate.

    Returns
    -------
    tuple
        * The vertices of the triangulation.
        * The faces of the triangulation.

    References
    ----------
    https://www.cs.cmu.edu/~quake/triangle.delaunay.html

    """
    data = {"vertices": [point[0:2] for point in points]}
    result = triangulate(data, opts="c")
    vertices = [[x, y, 0.0] for x, y in result["vertices"]]
    faces = result["triangles"]
    return vertices, faces


@plugin(category="triangulation")
def constrained_delaunay_triangulation(
    boundary: list[Point],
    polylines: Optional[list[Polyline]] = None,
    polygons: Optional[list[Polygon]] = None,
) -> tuple[list[Point], list[Triangle]]:
    """Construct a Delaunay triangulation of set of vertices, constrained to the specified segments.

    Parameters
    ----------
    boundary : list
        Ordered points on the boundary.
    polylines : list, optional
        Lists of ordered points defining internal guide curves.
    polygons : list, optional
        Lists of ordered points defining holes in the triangulation.

    Returns
    -------
    tuple
        * The vertices of the triangulation.
        * The faces of the triangulation.

    Notes
    -----
    No additional points will be inserted in the triangulation.

    References
    ----------
    https://www.cs.cmu.edu/~quake/triangle.delaunay.html

    """
    vertices, segments, holes = _to_vertices_segments_holes(boundary, polylines, polygons)

    data = {"vertices": vertices, "segments": segments}

    if len(holes) > 0:
        data["holes"] = holes

    result = triangulate(data, opts="p")

    vertices = [[x, y, 0.0] for x, y in result["vertices"]]
    faces = result["triangles"]
    return vertices, faces


@plugin(category="triangulation")
def conforming_delaunay_triangulation(
    boundary: list[Point],
    polylines: Optional[list[Polyline]] = None,
    polygons: Optional[list[Polygon]] = None,
    angle: Optional[float] = None,
    area: Optional[float] = None,
) -> tuple[list[Point], list[Triangle]]:
    """Construct a Conforming Delaunay triangulation of set of vertices, constrained to the specified segments.

    Parameters
    ----------
    boundary : list
        Ordered points on the boundary.
    polylines : list, optional
        Lists of ordered points defining internal guide curves.
    polygons : list, optional
        Lists of ordered points defining holes in the triangulation.
    angle : float, optional
        Minimum angle constraint for the triangles of the triangulation.
        If an angle constraint is given, "Steiner points" may be inserted internally
        and along the constraint segments to satisfy the constraint.
        The angle constraint should be specified in degrees.
    area : float, optional
        Maximum area constraint for the triangles of the triangulation.
        If an area constraint is given, "Steiner points" may be inserted internally
        and along the constraint segments to satisfy the constraint.

    Returns
    -------
    tuple
        * The vertices of the triangulation.
        * The faces of the triangulation.

    References
    ----------
    https://www.cs.cmu.edu/~quake/triangle.delaunay.html

    """
    vertices, segments, holes = _to_vertices_segments_holes(boundary, polylines, polygons)

    data = {"vertices": vertices, "segments": segments}

    if len(holes) > 0:
        data["holes"] = holes

    opts = "pq"

    if angle:
        opts = "{}{}".format(opts, angle)

    if area:
        opts = "{}a{}".format(opts, area)

    if opts == "pq":
        opts = "pq0D"

    result = triangulate(data, opts=opts)

    vertices = [[x, y, 0.0] for x, y in result["vertices"]]
    faces = result["triangles"]
    return vertices, faces
