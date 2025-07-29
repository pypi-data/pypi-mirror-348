"""
Module for primitive geometries. This is used to keep dependencies simple,
consider a real geometry library like cgal for more complex or performance
dependent work.
"""

from __future__ import annotations
import copy
from dataclasses import dataclass


@dataclass(frozen=True)
class Vector:
    """
    A 3d spatial vector
    """

    x: float
    y: float = 0.0
    z: float = 0.0

    def scale(self, factor: float) -> Vector:
        return Vector(self.x * factor, self.y * factor, self.z * factor)


@dataclass(frozen=True)
class Point:
    """
    A location in 3d space
    """

    x: float
    y: float = 0.0
    z: float = 0.0

    def translate(self, v: Vector) -> Point:
        return Point(self.x + v.x, self.y + v.y, self.z + v.z)


@dataclass(frozen=True)
class Shape:
    """
    A shape in 3d space, defaults to having a normal to Z
    """

    loc: Point
    normal: Vector = Vector(0.0, 0.0, 1.0)


@dataclass(frozen=True)
class Quad(Shape):
    """
    A regular quadrilateral in 3d space, defaults to be normal to Z
    """

    width: float = 1.0
    height: float = 1.0

    @property
    def points(self) -> list[Point]:
        p = copy.deepcopy(self.loc)
        return [
            p,
            p.translate(Vector(self.width)),
            p.translate(Vector(self.width, self.height)),
            p.translate(Vector(0.0, self.height)),
        ]

    def translate(self, v: Vector) -> Quad:
        return Quad(self.loc.translate(v), self.normal, self.width, self.height)


@dataclass(frozen=True)
class Cuboid(Shape):
    """
    A regular cuboid
    """

    loc: Point
    width: float = 1.0
    height: float = 1.0
    depth: float = 1.0

    def translate(self, v: Vector) -> Cuboid:
        return Cuboid(
            self.loc.translate(v), self.normal, self.width, self.height, self.depth
        )

    @property
    def points(self) -> list[Point]:

        base = Quad(self.loc, self.normal, self.width, self.height)
        top = base.translate(self.normal.scale(self.depth))
        return base.points + top.points


@dataclass(frozen=True)
class Cylinder(Shape):
    """
    A cylinder
    """

    diameter: float = 1.0
    length: float = 1.0

    @property
    def start(self) -> Point:
        return self.loc

    @property
    def end(self) -> Point:
        return self.loc.translate(self.normal.scale(self.length))


@dataclass(frozen=True)
class Revolution(Shape):
    """
    A revolved profile sitting on the plane given by the loc
    and normal and revolved about the normal.
    """

    diameter: float = 1.0
    length: float = 1.0
    profile: str = "arc"


@dataclass(frozen=True)
class CuboidGrid:
    """
    A irregular grid composed of cuboids. Can be useful for
    generating topological meshes like OpenFoam's blockMesh.
    """

    x_locs: list[float]
    y_locs: list[float]
    z_locs: list[float]

    @property
    def cuboids(self) -> list[Cuboid]:
        ret = []

        for kdx, z in enumerate(self.z_locs[:-1]):
            for jdx, y in enumerate(self.y_locs[:-1]):
                for idx, x in enumerate(self.x_locs[:-1]):
                    width = self.x_locs[idx + 1] - x
                    height = self.y_locs[jdx + 1] - y
                    depth = self.z_locs[kdx + 1] - z
                    ret.append(
                        Cuboid(Point(x, y, z), width=width, height=height, depth=depth)
                    )
        return ret
