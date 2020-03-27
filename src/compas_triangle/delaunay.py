from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from triangle import triangulate
from compas.utilities import pairwise
from compas.utilities import geometric_key_xy as geo
from compas.geometry import centroid_points_xy


__all__ = [
    'delaunay_triangulation',
    'constrained_delaunay_triangulation',
]


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


def constrained_delaunay_triangulation(boundary, polylines=None, polygons=None, area=None):
    """Construct a Delaunay triangulation of set of vertices, constrained to the specified segments.

    Parameters
    ----------
    boundary : list
        Ordered points on the boundary.
    polylines : list, optional
        Lists of ordered points defining internal guide curves.
    polygons : list, optional
        Lists of ordered points defining holes in the triangulation.
    area : float, optional
        Area constraint for the triangulation.

    Returns
    -------
    tuple
        * The vertices of the triangulation.
        * The faces of the triangulation.

    Notes
    -----
    No additional vertices (Steiner points) will be inserted.
    Therefore not all faces of the triangulation will be Delaunay.

    Examples
    --------
    >>>

    References
    ----------
    https://www.cs.cmu.edu/~quake/triangle.delaunay.html

    """
    gkey_xyz = {geo(point): point[:2] for point in boundary}

    if polylines:
        for polyline in polylines:
            gkey_xyz.update({geo(point): point[:2] for point in polyline})
    if polygons:
        for polygon in polygons:
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

    data = {'vertices': vertices, 'segments': segments, 'holes': holes}
    if area:
        result = triangulate(data, opts='pa{}q'.format(area))
    else:
        result = triangulate(data, opts='pq')
    vertices = [[x, y, 0] for x, y in result['vertices']]
    faces = result['triangles']
    return vertices, faces


# def conforming_delaunay_triangulation(points, segments):
#     """Construct a Delaunay triangulation of set of vertices,
#     constrained to the specified segments,
#     and with as many Steiner points inserted as necessary to make sure all faces
#     of the triangulation are Delaunay.

#     Parameters
#     ----------
#     points : list
#         XY(Z) coordinates of the points to triangulate.
#     segments : list
#         A list of point index pairs, to indicate which straight line segments
#         should be included in the triangulation.

#     Returns
#     -------
#     tuple
#         The vertices of the triangulation and the faces of the triangulation.

#     Notes
#     -----
#     Concavities will be removed automatically.
#     Therefore, the boundary of the triangulation should be included in the specification
#     of segments to avoid unexpected results.

#     References
#     ----------
#     https://www.cs.cmu.edu/~quake/triangle.delaunay.html

#     Examples
#     --------
#     >>>

#     """
#     data = {'vertices': [point[0:2] for point in points], 'segments': segments}
#     result = triangulate(data, opts='pq0D')
#     vertices = [[x, y, 0.0] for x, y in result['vertices']]
#     faces = result['triangles']
#     return vertices, faces


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    pass
