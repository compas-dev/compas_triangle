from compas.datastructures import Mesh
from compas.geometry import Polygon
from compas.geometry import Translation
from compas_viewer import Viewer

from compas_triangle.delaunay import conforming_delaunay_triangulation

# ==============================================================================
# Constraints
# ==============================================================================

boundary = Polygon.from_sides_and_radius_xy(4, 10)
boundary = list(boundary)

hole = Polygon.from_sides_and_radius_xy(8, 2)

hole1 = hole.transformed(Translation.from_vector([4, 0, 0]))
hole2 = hole.transformed(Translation.from_vector([-4, 0, 0]))
hole3 = hole.transformed(Translation.from_vector([0, 4, 0]))
hole4 = hole.transformed(Translation.from_vector([0, -4, 0]))

holes = [list(hole1), list(hole2), list(hole3), list(hole4)]

# ==============================================================================
# Triangulation
# ==============================================================================

V, F = conforming_delaunay_triangulation(boundary, polygons=holes, area=0.3)

mesh = Mesh.from_vertices_and_faces(V, F)

# ==============================================================================
# Viz
# ==============================================================================

viewer = Viewer()
viewer.scene.add(mesh, show_points=True)
viewer.show()
