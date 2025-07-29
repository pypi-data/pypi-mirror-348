"""
Meshing utilities for use in openfoam
"""

from .mesh import Mesh


def mesh_to_foam(mesh: Mesh) -> str:
    """
    Given a mesh, write it in openfoam blockMesh format
    """

    output = f"scale\t{mesh.scale}\n"

    output += "vertices\n(\n"
    for idx, v in enumerate(mesh.vertices):
        output += f"\t( {v.x} {v.y} {v.z} ) // # {idx} \n"
    output += ");\n\n"

    output += "edges\n(\n"
    for e in mesh.edges:
        if e.type == "line":
            output += f"\tline {e.vert0} {e.vert1}\n"
        else:
            interps = ""
            for p in e.interp_points:
                interps += f"({p.x} {p.y} {p.z}) "
            output += f"\t {e.type} {e.vert0} {e.vert1} {interps}\n"
    output += ");\n\n"

    output += "blocks\n(\n"
    for b in mesh.blocks:
        verts = " ".join(str(v) for v in b.vertices)
        output += f"\thex({verts})\n"

        counts = " ".join(str(c) for c in b.cell_counts)
        output += f"\t({counts})\n"

        grades = " ".join(str(g) for g in b.grading_ratios)
        output += f"\t{b.grading} ({grades})\n"
    output += ");\n\n"

    output += "boundary\n(\n"
    for patch in mesh.patches:
        output += f"\t{patch.name}\n"
        output += "\t{\n"
        output += f"\t\ttype {patch.type};\n"
        output += "\t\tfaces\n\t\t(\n"
        for f in patch.faces:
            faces = " ".join(str(idx) for idx in f)
            output += f"\t\t\t({faces})\n"
        output += "\t\t);\n"
        output += "\t}\n"
    output += ");\n\n"

    return output
