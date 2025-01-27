from compas.datastructures import Mesh
from compas_viewer import Viewer

from compas_triangle.delaunay import delaunay_triangulation

points = [
    [2.994817685045075, 10.855606612493078, 0.0],
    [4.185204599300653, 9.527867361977242, 0.0],
    [4.414125159734419, 10.718254276232818, 0.0],
    [5.925000858597267, 9.344730913630228, 0.0],
    [8.900968144236211, 10.809822500406325, 0.0],
    [9.496161601363999, 8.566401008155429, 0.0],
    [7.710581229980631, 7.9254234389408875, 0.0],
    [7.847933566240888, 6.414547740078039, 0.0],
    [3.9104999267801377, 4.9036720412151915, 0.0],
    [5.2909301507195865, 6.342692886748852, 0.0],
]

vertices, faces = delaunay_triangulation(points)

mesh = Mesh.from_vertices_and_faces(vertices, faces)

viewer = Viewer()
viewer.scene.add(mesh, show_points=True)
viewer.show()
