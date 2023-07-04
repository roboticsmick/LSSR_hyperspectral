import os
from openhsi.capture import *
from openhsi.cameras import *
import matplotlib.pyplot as plt

# Get the current working directory
CWD = os.getcwd()
ASSETS_FOLDER = os.path.join(CWD, "assets")
JSON_FILE = "OpenHSI-06_settings_Mono12_bin2.json"
PKL_FILE = "OpenHSI-06_calibration_Mono12_bin2.pkl"
json_path = os.path.join(ASSETS_FOLDER, JSON_FILE)
pkl_path = os.path.join(ASSETS_FOLDER, PKL_FILE)

with LucidCamera(
    n_lines = 1000,
    processing_lvl = -1,
    pkl_path = pkl_path,
    json_path = json_path
                ) as cam:
    cam.collect()
    fig = cam.show(plot_lib="matplotlib", robust=True)
     
fig


# import os
# from openhsi.capture import *
# from openhsi.cameras import LucidCamera
# import matplotlib.pyplot as plt

# # Get the current working directory
# CWD = os.getcwd()
# ASSETS_FOLDER = os.path.join(CWD, "assets")
# JSON_FILE = "OpenHSI-06_settings_Mono8_bin1.json"
# PKL_FILE = "OpenHSI-06_calibration_Mono8_bin1.pkl"
# json_path = os.path.join(ASSETS_FOLDER, JSON_FILE)
# pkl_path = os.path.join(ASSETS_FOLDER, PKL_FILE)

# IMG_FILE = "test_img.jpg"
# TES_IMG = os.path.join(ASSETS_FOLDER, IMG_FILE)

# with SimulatedCamera(
#     n_lines=1024,
#     processing_lvl=3,
#     pkl_path=pkl_path,
#     json_path=json_path,

# ) as cam:
#     cam.collect()
#     fig = cam.show(plot_lib="matplotlib", robust=True)

# fig.opts(fig_inches=7,title="simulated hyperspectral datacube")