import compas_rhino.conversions
import compas_rhino.objects
import rhinoscriptsyntax as rs  # type: ignore
from compas.geometry import Curve


def guid_to_compas_curve(guid) -> Curve:
    return compas_rhino.conversions.curveobject_to_compas(compas_rhino.objects.find_object(guid))


def discretise_boundary(guids, length):
    boundary = []
    for guid in guids:
        rs.EnableRedraw(False)

        segments = rs.ExplodeCurves(guid)
        for segment in segments:
            curve: Curve = guid_to_compas_curve(segment)
            N = int(curve.length() / length)
            _, points = curve.divide_by_count(N, return_points=True)
            boundary.extend(map(list, points))

        rs.DeleteObjects(segments)
        rs.EnableRedraw(True)
    return boundary


def discretise_constraints(guids, length):
    polylines = []
    if guids:
        for guid in guids:
            curve: Curve = guid_to_compas_curve(guid)
            N = int(curve.length() / length)
            _, points = curve.divide_by_count(N, return_points=True)
            polylines.append(map(list, points))
    return polylines
