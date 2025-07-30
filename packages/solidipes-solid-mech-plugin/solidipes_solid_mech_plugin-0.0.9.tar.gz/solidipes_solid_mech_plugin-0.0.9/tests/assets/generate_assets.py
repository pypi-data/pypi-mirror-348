import pyvista as pv


def main():
    generate_pyvista_assets()


def generate_pyvista_assets():
    generate_vtu()
    generate_pyvista_plot()


def generate_vtu():
    points = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]]
    cells = [3, 0, 1, 2]
    cell_types = [pv.CellType.TRIANGLE]

    mesh = pv.UnstructuredGrid(cells, cell_types, points)
    mesh.point_data.set_array([1, 2, 3], "point 1D")
    mesh.point_data.set_array(pv.pyvista_ndarray([[1, 2, 3], [4, 5, 6], [7, 8, 9]]), "point 3D")
    mesh.cell_data.set_array([1], "cell 1D")
    mesh.cell_data.set_array(pv.pyvista_ndarray([[1, 2, 3]]), "cell 3D")

    mesh.save("pyvista_mesh.vtu")


def generate_pyvista_plot():
    mesh = pv.read("pyvista_mesh.vtu")
    plotter = pv.Plotter(off_screen=True)
    plotter.background_color = "black"
    plotter.add_mesh(mesh)
    plotter.screenshot("pyvista_plot.png", window_size=(50, 50))


if __name__ == "__main__":
    main()
