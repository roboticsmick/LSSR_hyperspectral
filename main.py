import os
from openhsi.capture import SimulatedCamera
import matplotlib.pyplot as plt

# Settings file locations
assets_folder = os.path.join(os.path.dirname(__file__), "assets")
json_filename = "cam_settings.json"
pkl_filename = "cam_calibration.pkl"

# Image file locations
image_folder = os.path.join(os.path.dirname(__file__), "images")
img_filename = "rocky_beach.png"


with SimulatedCamera(
    img_path=os.path.join(image_folder, img_filename),
    n_lines=1024,
    processing_lvl=3,
    json_path=os.path.join(assets_folder, json_filename),
    pkl_path=os.path.join(assets_folder, pkl_filename)
) as cam:
    cam.collect()
    fig = cam.show(plot_lib="matplotlib", robust=True)
    plt.show()
