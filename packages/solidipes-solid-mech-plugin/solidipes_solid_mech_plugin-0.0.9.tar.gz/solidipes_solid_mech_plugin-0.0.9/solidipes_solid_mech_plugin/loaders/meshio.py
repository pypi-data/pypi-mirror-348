from solidipes.loaders.file import File


class Meshio(File):
    """File loaded with meshio"""

    def __init__(self, **kwargs):
        from ..viewers.pyvista_plotter import PyvistaPlotter

        super().__init__(**kwargs)
        self.compatible_viewers[:0] = [PyvistaPlotter]

    @File.loadable
    def mesh(self):
        import meshio

        return meshio.read(self.file_info.path)
