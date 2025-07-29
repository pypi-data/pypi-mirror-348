"""
Module for describing mesh elements. Goes for simplicity and low dependencies
over performance. Consider something else for high performance meshing.
"""

from __future__ import annotations
from dataclasses import dataclass

from icplot.geometry import Point, Cuboid


@dataclass(frozen=True)
class Vertex:
    """
    A mesh vertext
    """

    x: float
    y: float
    z: float = 0.0

    @staticmethod
    def from_point(p: Point) -> Vertex:
        return Vertex(p.x, p.y, p.z)


@dataclass(frozen=True)
class Edge:
    """
    A mesh edge - consists of two verts
    """

    vert0: int
    vert1: int
    type: str = "line"
    interp_points: tuple[Point, ...] = ()


@dataclass(frozen=True)
class Block:
    """
    A hex mesh element - used in openfoam meshing
    """

    vertices: tuple[int, ...]
    cell_counts: tuple[int, ...] = (1, 1, 1)
    grading: str = "simple"
    grading_ratios: tuple[int, ...] = (1, 1, 1)


@dataclass(frozen=True)
class Patch:
    """
    A collection of mesh faces - used for openfoam boundaries
    """

    type: str
    name: str
    faces: tuple[tuple[int, ...], ...]


@dataclass(frozen=True)
class Mesh:
    """
    A mesh tailored for use in openfoam
    """

    vertices: tuple[Vertex, ...]
    blocks: tuple[Block, ...]
    edges: tuple[Edge, ...] = ()
    patches: tuple[Patch, ...] = ()
    scale: float = 1.0


def from_cuboid(cuboid: Cuboid) -> Mesh:

    verts = tuple(Vertex.from_point(p) for p in cuboid.points)
    blocks = (Block(tuple(range(len(verts)))),)
    return Mesh(verts, blocks)
