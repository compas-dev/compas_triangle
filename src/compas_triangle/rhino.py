from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rhino.geometry import RhinoCurve


__all__ = ['discretise_boundary']


def discretise_boundary(guids, length):
    boundary = []
    for guid in guids:
        compas_rhino.rs.EnableRedraw(False)
        segments = compas_rhino.rs.ExplodeCurves(guid)
        for segment in segments:
            curve = RhinoCurve.from_guid(segment)
            N = int(curve.length() / length)
            points = curve.divide(N, over_space=True)
            boundary.extend(map(list, points))
        compas_rhino.rs.DeleteObjects(segments)
        compas_rhino.rs.EnableRedraw(True)
    return boundary


def discretise_constraints(guids, length):
    polylines = []
    if guids:
        for guid in guids:
            curve = RhinoCurve.from_guid(guid)
            N = int(curve.length() / length)
            points = curve.divide(N, over_space=True)
            polylines.append(map(list, points))
    return polylines


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
