import os
import json
import compas
from compas.datastructures import Mesh
from compas.geometry import centroid_points_xy
from compas_plotters import MeshPlotter
from compas.utilities import geometric_key
from compas.utilities import pairwise
from compas_triangle.delaunay import constrained_delaunay_triangulation


HERE = os.path.dirname(__file__)
DATA = os.path.join(HERE, '../data')
FILE = os.path.join(DATA, 'rhino.json')

with open(FILE, 'r') as f:
    data = json.load(f)

boundary = data['boundary']
polylines = [data['segments']]
polygons = [data['hole']]

V2, F2 = constrained_delaunay_triangulation(boundary, polylines, polygons, area=0.05)

mesh = Mesh.from_vertices_and_faces(V2, F2)

lines = []

for a, b in pairwise(boundary):
    lines.append({'start': a, 'end': b, 'color': '#ff0000', 'width': 2.0})

for polyline in polylines:
    for a, b in pairwise(polyline):
        lines.append({'start': a, 'end': b, 'color': '#ff0000', 'width': 2.0})

for polygon in polygons:
    for a, b in pairwise(polygon):
        lines.append({'start': a, 'end': b, 'color': '#ff0000', 'width': 2.0})

plotter = MeshPlotter(mesh, figsize=(8, 5))
plotter.draw_faces()
plotter.draw_lines(lines)
plotter.show()
