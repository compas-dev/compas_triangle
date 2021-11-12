from compas.datastructures import Mesh
from compas.geometry import centroid_points_xy
from compas.utilities import geometric_key
from compas.utilities import pairwise
from compas.rpc import Proxy

import compas_rhino
from compas_rhino.geometry import RhinoCurve
from compas_rhino.artists import MeshArtist

from compas_triangle.rhino import discretise_boundary
from compas_triangle.rhino import discretise_constraints

# create a proxy for the delaunay module of compas_triangle
triangle = Proxy('compas_triangle.delaunay')
triangle.restart_server()

# set a target length
L = 0.5

# set an area constraint
A = L ** 2 * 0.5 * 0.5 * 1.732

# set an angle constraint
# warning: don't go crazy here because otherwise you will need MANY triangles to satisfy the constraint
Q = 30

# ask the user to select the boundaries, internal boundaries or "holes", and constraint curves
# note that the boundary is required
# however, the holes and constraint curves are optional
boundary_guids = compas_rhino.select_curves('Select boundary curves.')
compas_rhino.rs.UnselectAllObjects()

hole_guids = compas_rhino.select_curves('Select inner boundaries.')
compas_rhino.rs.UnselectAllObjects()

segments_guids = compas_rhino.select_curves('Select constraint curves.')
compas_rhino.rs.UnselectAllObjects()

# discretise the boundary according to the target length
boundary = discretise_boundary(boundary_guids, L)

# discretise the constraint curves
polylines = discretise_constraints(segments_guids, L)

# discretise the internal boundaries or "holes"
polygons = discretise_constraints(hole_guids, L)

# generate a Conforming Delaunay Triangulation
# use the angle constraint or the area constraint
# or both
vertices, faces = triangle.conforming_delaunay_triangulation(boundary, polylines, polygons, angle=Q)

# construct a COMPAS mesh from the triangulation
mesh = Mesh.from_vertices_and_faces(vertices, faces)

# visualize the mesh using an artist
artist = MeshArtist(mesh, layer="compas_triangle")
artist.clear_layer()
artist.draw_faces(join_faces=True)
