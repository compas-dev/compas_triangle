from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rhino.conversions import RhinoCurve


def discretise_boundary(guids, length):
    boundary = []
    for guid in guids:
        compas_rhino.rs.EnableRedraw(False)
        segments = compas_rhino.rs.ExplodeCurves(guid)
        for segment in segments:
            curve = RhinoCurve.from_guid(segment).to_compas()
            N = int(curve.length() / length)
            _, points = curve.divide_by_count(N, return_points=True)
            boundary.extend(map(list, points))
        compas_rhino.rs.DeleteObjects(segments)
        compas_rhino.rs.EnableRedraw(True)
    return boundary


def discretise_constraints(guids, length):
    polylines = []
    if guids:
        for guid in guids:
            curve = RhinoCurve.from_guid(guid).to_compas()
            N = int(curve.length() / length)
            _, points = curve.divide_by_count(N, return_points=True)
            polylines.append(map(list, points))
    return polylines
