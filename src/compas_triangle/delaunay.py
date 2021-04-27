from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from triangle import triangulate
from compas.utilities import pairwise
from compas.utilities import geometric_key_xy as geo
from compas.geometry import centroid_points_xy

from compas.plugins import plugin


__all__ = [
    'delaunay_triangulation',
    'constrained_delaunay_triangulation',
    'conforming_delaunay_triangulation',
]


def _to_vertices_segments_holes(boundary, polylines, polygons):
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


@plugin(category='triangulation')
def delaunay_triangulation(points):
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

    Examples
    --------
    >>>

    References
    ----------
    https://www.cs.cmu.edu/~quake/triangle.delaunay.html

    """
    data = {'vertices': [point[0:2] for point in points]}
    result = triangulate(data, opts='c')
    vertices = [[x, y, 0] for x, y in result['vertices']]
    faces = result['triangles']
    return vertices, faces


@plugin(category='triangulation')
def constrained_delaunay_triangulation(boundary, polylines=None, polygons=None):
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

    Examples
    --------
    >>>

    References
    ----------
    https://www.cs.cmu.edu/~quake/triangle.delaunay.html

    """
    vertices, segments, holes = _to_vertices_segments_holes(boundary, polylines, polygons)

    data = {'vertices': vertices, 'segments': segments}

    if len(holes) > 0:
        data['holes'] = holes

    result = triangulate(data, opts='p')

    vertices = [[x, y, 0.0] for x, y in result['vertices']]
    faces = result['triangles']
    return vertices, faces


@plugin(category='triangulation')
def conforming_delaunay_triangulation(boundary, polylines=None, polygons=None, angle=None, area=None):
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

    Examples
    --------
    >>>

    References
    ----------
    https://www.cs.cmu.edu/~quake/triangle.delaunay.html

    """
    vertices, segments, holes = _to_vertices_segments_holes(boundary, polylines, polygons)

    data = {'vertices': vertices, 'segments': segments}

    if len(holes) > 0:
        data['holes'] = holes

    opts = 'pq'

    if angle:
        opts = '{}{}'.format(opts, angle)

    if area:
        opts = '{}a{}'.format(opts, area)

    if opts == 'pq':
        opts = 'pq0D'

    result = triangulate(data, opts=opts)

    vertices = [[x, y, 0] for x, y in result['vertices']]
    faces = result['triangles']
    return vertices, faces


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    pass
