import pyvista as pv
import solidipes as sp
import utils
from PIL import Image
from pixelmatch.contrib.PIL import pixelmatch

image_name = "pyvista_plot.png"
image_size = (1024, 768)


def test_plotter(study_dir):
    pyvista_file = sp.load_file(utils.get_asset_path("pyvista_mesh.vtu"))
    test_image_path = study_dir / image_name
    reference_image_path = utils.get_asset_path(image_name)

    # Start virtual frame buffer, otherwise segfault
    pv.start_xvfb()

    # Create a plotter and save the image
    plotter = sp.viewer.PyvistaPlotter(off_screen=True)
    plotter.add_mesh(pyvista_file)
    plotter.show()  # Not shown because off_screen=True
    plotter.save(test_image_path)

    test_image = Image.open(test_image_path)
    reference_image = Image.open(reference_image_path)
    diff = Image.new("RGB", image_size)
    mismatch = pixelmatch(test_image, reference_image, diff)
    assert mismatch == 0
