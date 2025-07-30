import pytest
import pyvista as pv
import solidipes as sp
import utils


@pytest.fixture
def file(study_dir):
    file_path = utils.get_asset_path("pyvista_mesh.vtu")
    file = sp.load_file(file_path)
    file.load_all()
    return file


def test_point_data(file):
    """Test .add_point_data, .get_point_data, and .remove_point_data"""

    # Test .add_point_data
    new_data = [4, 5, 6]
    new_data_name = "new point data"
    file.add_point_data(new_data, new_data_name)
    assert new_data_name in file.point_data_names

    # Test .get_point_data
    assert file.get_point_data(new_data_name).tolist() == new_data

    # Test .remove_point_data
    file.remove_point_data(new_data_name)
    assert new_data_name not in file.point_data_names


def test_cell_data(file):
    """Test .add_cell_data, .get_cell_data, and .remove_cell_data"""

    # Test .add_cell_data
    new_data = [2]
    new_data_name = "new cell data"
    file.add_cell_data(new_data, new_data_name)
    assert new_data_name in file.cell_data_names

    # Test .get_cell_data
    assert file.get_cell_data(new_data_name).tolist() == new_data

    # Test .remove_cell_data
    file.remove_cell_data(new_data_name)
    assert new_data_name not in file.cell_data_names


def test_get_data(file):
    """Test getting data by name"""

    # Test mesh
    data = file.get("mesh")
    assert isinstance(data, pv.UnstructuredGrid)

    assert data is file.pyvista_mesh
    assert data.points.tolist() == [
        [0.0, 0.0, 0.0],
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
    ]
    assert data.cells.tolist() == [3, 0, 1, 2]

    # Test point data
    data = file.get("point 1D (point data)")
    assert data.tolist() == [1, 2, 3]

    data = file.get("point 3D (point data)")
    assert data.tolist() == [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

    # Test cell data
    data = file.get("cell 1D (cell data)")
    assert data.tolist() == [1]

    data = file.get("cell 3D (cell data)")
    assert data.tolist() == [[1, 2, 3]]

    # Test invalid data name
    with pytest.raises(KeyError):
        file.get("invalid data name")


def test_get_warped(file):
    """Test .get_warped and @get_point_data_from_id_or_array decorator"""

    # Warp by scalar
    warped = file.get_warped("point 1D")
    assert warped.pyvista_mesh.points.tolist() == [
        [0.0, 0.0, 1.0],
        [1.0, 0.0, 2.0],
        [0.0, 1.0, 3.0],
    ]

    # Warp by vector
    warped = file.get_warped("point 3D")
    assert warped.pyvista_mesh.points.tolist() == [
        [1.0, 2.0, 3.0],
        [5.0, 5.0, 6.0],
        [7.0, 9.0, 9.0],
    ]

    # Warp by external array
    array = [1, 2, 3]
    warped = file.get_warped(array)
    assert warped.pyvista_mesh.points.tolist() == [
        [0.0, 0.0, 1.0],
        [1.0, 0.0, 2.0],
        [0.0, 1.0, 3.0],
    ]


def test_set_values(file):
    """Test .set_point_values, .set_cell_values, and
    @get_cell_data_from_id_or_array decorator"""

    # Set point data
    file.set_point_values("point 1D")
    assert file.pyvista_mesh.active_scalars_name == "point 1D"

    # Set cell data
    file.set_cell_values("cell 1D")
    assert file.pyvista_mesh.active_scalars_name == "cell 1D"

    # Attempt invalid data names
    with pytest.raises(ValueError):
        file.set_point_values("cell 1D")

    with pytest.raises(ValueError):
        file.set_cell_values("point 1D")

    # Set external array
    array = [1]
    file.set_cell_values(array)
    assert file.pyvista_mesh.active_scalars.tolist() == array
