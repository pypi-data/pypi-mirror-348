from .parse_inp import read_geof
from .pyvista_mesh import PyvistaMesh


class GeofMesh(PyvistaMesh):
    """Mesh file loaded with pyvista"""

    supported_mime_types = {"meshing/z-set": "geof"}

    @PyvistaMesh.loadable
    def mesh(self):
        from pyvista.core.utilities import from_meshio

        return from_meshio(read_geof(self.file_info.path))
