import os

from solidipes.loaders.data_container import DataContainer
from solidipes.viewers import backends as viewer_backends
from solidipes.viewers.viewer import Viewer

from .. import config

os.environ["STREAMLIT_PYVISTA_CACHE_DIR_NAME"] = config.streamlit_pyvista_cache_dir_name


class PyvistaPlotter(Viewer):
    """Viewer for pyvista meshes

    Args:
        **kwargs: keyword arguments passed to the pyvista.Plotter constructor
    """

    def __init__(self, data_container=None, add_kwargs={}, show_kwargs={}, **kwargs):
        import pyvista as pv

        #: keeps track of whether the plotter has already been shown
        self.shown = False

        #: Pyvista plotter
        self.plotter = None
        if viewer_backends.current_backend == "streamlit":
            self.plotter = pv.Plotter(off_screen=True, **kwargs)
        else:  # python or jupyter notebook
            self.plotter = pv.Plotter(**kwargs)

        self.plotter.background_color = "black"
        self.meshes = []
        self.points = []
        self.path_list = []
        self._update_path_list(data_container)
        super().__init__(data_container, add_kwargs=add_kwargs, show_kwargs=show_kwargs)

    def add(self, data_container, **kwargs):
        """Add mesh to the viewer

        Args:
            **kwargs: keyword arguments passed to the pyvista.Plotter.add_mesh
                method
        """
        from ..loaders.abaqus import Abaqus

        self.check_data_compatibility(data_container)

        if isinstance(data_container, Abaqus):
            for name, m in data_container.meshes.items():
                self.meshes.append((m, kwargs))

        elif isinstance(data_container, DataContainer):
            self.add_mesh(data_container, **kwargs)

    def add_mesh(self, data_container: DataContainer, **kwargs):
        """Add mesh to the viewer

        Args:
            **kwargs: keyword arguments passed to the pyvista.Plotter.add_mesh
                method
        """
        data = data_container.mesh
        self.meshes.append((data, kwargs))
        self._update_path_list(data_container)

    def _update_path_list(self, data_container):
        from solidipes.loaders.file_sequence import FileSequence

        if isinstance(data_container, FileSequence):
            path = data_container.paths.copy()
            self.path_list = path
        else:
            if data_container is not None:
                path = data_container.file_info.path
                self.path_list.append(path)

    def add_points(self, data_container, **kwargs):
        """Add mesh as points to the viewer

        Args:
            **kwargs: keyword arguments passed to the
                pyvista.Plotter.add_points method
        """
        data = data_container.mesh
        self.points.append((data, kwargs))

    def show(self, auto_close=False, **kwargs):
        """Show the viewer

        Args:
            auto_close: whether to close the viewer after showing it
            **kwargs: keyword arguments passed to the pyvista.Plotter.show
                method
        """
        from streamlit_pyvista.mesh_viewer_component import MeshViewerComponent  # noqa: E402
        from streamlit_pyvista.server_managers import ServerManagerProxified  # noqa: E402
        from streamlit_pyvista.trame_viewers import get_advanced_viewer_path  # noqa: E402

        max_frames = 500
        paths = self.path_list
        if len(self.path_list) > max_frames:
            freq = len(self.path_list) / max_frames
            paths = paths[:: int(freq)]

        for p, _kwargs in self.points:
            self.plotter.add_points(p, **_kwargs)

        for m, _kwargs in self.meshes:
            self.plotter.add_mesh(m, **_kwargs)

        if viewer_backends.current_backend == "streamlit":
            key = f"pyvista_ploter_{paths[0]}"
            import streamlit as st

            for p, _ in self.points:
                st.write(p)

            # Display arrays of the raw data
            for i, (m, kw) in enumerate(self.meshes):
                options_key = key + f"mesh_{i}_options"
                if options_key not in st.session_state:
                    st.session_state[options_key] = ["None"] + m.array_names

                st.write(m)

            if len(paths) == 0:
                st.error("No mesh passed to the PyvistaPlotter")
                return

            self.shown = True
            MeshViewerComponent(
                paths,
                trame_viewer_class=get_advanced_viewer_path(),
                server_manager_class=ServerManagerProxified,
            ).show()
        elif viewer_backends.current_backend == "python":
            self.shown = True
            self.plotter.show(kwargs)
        else:
            self.shown = True
            MeshViewerComponent(
                paths,
                trame_viewer_class=get_advanced_viewer_path(),
                server_manager_class=ServerManagerProxified,
            ).show()

    def save(self, path, **kwargs):
        """Save the view to a file

        Args:
            path: path to the file
            **kwargs: keyword arguments passed to the
                pyvista.Plotter.screenshot method
        """
        # Pyvista Plotter must be shown before saving
        if not self.shown:
            self.plotter.show(auto_close=False)  # also for streamlit backend
            self.shown = True
        self.plotter.screenshot(path, **kwargs)
