import pytest
import pyvista as pv
import solidipes as sp
import utils


@pytest.fixture
def file(study_dir):
    file_path = utils.get_asset_path("xdmf_mesh.xdmf")
    file = sp.load_file(file_path)
    file.load_all()
    return file


def test_get_data(file):
    """Test getting data by name"""

    # Test mesh
    data = file.mesh
    assert isinstance(data, pv.UnstructuredGrid)

    assert data is file.mesh
    assert file.n_frames == 21
    assert data.points.tolist() == [
        [0.0, 0.0, 0.0],
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
    ]
    assert data.cells.tolist() == [3, 0, 1, 2]

    # Test invalid data name
    with pytest.raises(KeyError):
        file.get("invalid data name")
