from icplot.geometry import Point, Cuboid
from icplot.mesh import foam, from_cuboid


def test_mesh():

    cuboid = Cuboid(Point(0.0, 0.0, 0.0))

    mesh = from_cuboid(cuboid)

    foam_str = foam.mesh_to_foam(mesh)

    assert foam_str
