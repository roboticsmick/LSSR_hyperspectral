# LSSR_hyperspectral

## OpenHSI LucidCamera

[2022 RobotX Challenge TeamTime: OpenHSI explanation (starts at: 2:47)](https://youtu.be/jrBuJBmjm3Y?t=167)
[RobotX Resources Page: OpenHSI Resources](https://robotx.org/programs/robotx-challenge-2022/#resources)
[OpenHSI Technical summary](https://www.dropbox.com/s/3akr8s9h111yi2i/OpenHSI_Tech_summary.pdf?dl=0)

| SENSOR PROPERTIES |  |
|---|---|
| Sensor Model | Sony IMX273 CMOS |
| Shutter Type | Global |
| Sensor Size | 6.3 mm (Type 1/2.9″) |
| Resolution | 1440 x 1080 px, 1.6 MP |
| Pixel Size | 3.45 µm (H) x 3.45 µm (V) |
| Framerate* | 71.6 FPS (75.8 FPS) @ 1.6 MP |

| PHYSICAL PROPERTIES |  |
|---|---|
| Dimensions | 24 x 24 x 27.35 mm |
| Lens Mount | C, NF, S, No mount, C-Mount Extended Head |
| Weight | 30 g |

| INTERFACE AND POWER INFORMATION |  |
|---|---|
| Digital Interface | 1000BASE-T RJ45, PoE<br>ix Industrial, PoE<br>FFC, PoE |
| GPIO Interface | 8 pin JST connector |
| Opto-Isolated I/O Ports | 1 input, 1 output |
| Non-Isolated I/O Ports | 2 bi-directional |
| Power Requirement | PoE (IEEE 802.3af), or 12-24 VDC external |
| Power Consumption | 3.1W via PoE, 2.5W when powered externally |

## Software setup Ubuntu 22.10

[OpenHSI: Quick start guide](https://openhsi.github.io/openhsi/quick_start.html)

```sh
sudo apt install python3-venv
sudo apt install nodejs
```

```sh
git clone git@github.com:roboticsmick/LSSR_hyperspectral.git
cd LSSR_hyperspectral
python3 -m venv venv
source venv/bin/activate
```

### Install libraries

```sh
pip install --upgrade pip
pip install numpy
pip install matplotlib
pip install opencv-python
pip install openhsi
pip install spectral
pip install Pillow
pip install jupyterlab
pip install jupyter_bokeh
```

Error in OpenHSI library:
Change the camera.py file to:

```py
# These were around the wrong way
class LucidCamera(LucidCameraBase, OpenHSI):
```

Install Compilers:

```sh
cd
sudo apt update
sudo apt install make
sudo apt install build-essential
sudo apt install gfortran # Install Fortran compiler if not installed
sudo apt install micro
```

### Updating requirements.txt

```sh
pip install pipreqs
# Run in current directory
python3 -m  pipreqs.pipreqs .
```

### Install Arena SDK for LucidCamera

There are two files to download from Lucid Vision Labs:

1. Arena SDK
2. Arena Python Package

[Lucid Vision Labs Downloads](https://thinklucid.com/downloads-hub/)

```sh
cd ~/Downloads
tar -xf  ArenaSDK_v0.1.68_Linux_x64.tar.gz
mv ~/Downloads/ArenaSDK_Linux_x64 ~/LSSR_hyperspectral/assets/
cd ~/LSSR_hyperspectral/assets/ArenaSDK_Linux_x64
sudo sh Arena_SDK_Linux_x64.conf
```

```sh
cd ~/Downloads
unzip arena_api-2.3.3-py3-none-any.zip -d arena_api-2.3.3-py3-none-any
mv ~/Downloads/arena_api-2.3.3-py3-none-any ~/LSSR_hyperspectral/assets/
cd ~/LSSR_hyperspectral/assets/arena_api-2.3.3-py3-none-any
pip install arena_api-2.3.3-py3-none-any.whl
```

#### Jumbo Frames

Setup jumbo frames for the ethernet connection. This isn't permanent (work out how to set it up to run at startup later).

Get the ethernet adaptor address. You will need this value for a number of the steps below.

```sh
sudo apt install net-tools
ip link show | grep mtu # Copy the ethernet address (e.g enp2s0)
sudo ifconfig enp2s0 mtu 9000 # Change enp2s0 to the value in the previous step
```

#### Adjust the receive buffer size

These were the values I initially recieved for my network card. My RX had a pre-set limit of 256. This means I couldn't update it based on the instructions on OpenHSI to 4096.

```sh
# Look for the enXXXX value that corresponds to the ethernet network card address
# My ethernet address was enp2s0
sudo apt install ethtool        
# Take a note of the pre-set maximum for RX. 
# This is the highest you can set the RX too.
sudo ethtool -g enp2s0  # Edit the ethernet address
```

```sh
Ring parameters for enp2s0:
Pre-set maximums:
RX: 256
RX Mini: n/a
RX Jumbo: n/a
TX: 256
Current hardware settings:
RX:  256
RX Mini: n/a
RX Jumbo: n/a
TX: 256
RX Buf Len: n/a
CQE Size: n/a
TX Push: off
```

Updating my ethernet driver allowed me to increase it to 1024.

```sh
# This will give the details of the ethernet controller in your PC
lspci | grep -i net
# Mine was:
# Ethernet controller: Realtek Semiconductor Co., Ltd. RTL8111/8168/8411 PCI Express Gigabit Ethernet Controller (rev 15)
```

I was able to find a newer driver by Realtek r8168-8.051.02. Updating the driver increased my pre-set RX maximum to 1024. I

```sh
sudo ethtool -g enp2s0  # Edit the ethernet address
sudo ethtool -G enp2s0 rx 1024  # I wasn't able to set me rx to 4096 as directed by the OpenHSI and Lucid Vision Labs instructions. If you can, update to 4096. 
```

#### Set the socket buffer size

```sh
sudo sh -c "echo 'net.core.rmem_default=1048576' >> /etc/sysctl.conf"
sudo sh -c "echo 'net.core.rmem_max=1048576' >> /etc/sysctl.conf"
sudo sysctl -p
```

To make these changes permanent, edit the conf file by commenting out the last two lines:

```sh
 sudo micro /etc/sysctl.d/10-network-security.conf
```

```sh
sudo sysctl -w net.ipv4.conf.default.rp_filter=0
sudo sysctl -w net.ipv4.conf.all.rp_filter=0
sudo sysctl -w net.ipv4.conf.enp2s0.rp_filter=0 # Edit the ethernet address
```

```sh
# Enter root
sudo -i
apt-get install ufw -y
ufw enable
ufw status
ufw allow 3956/udp
ufw allow 49152:65534/udp
ufw status verbose
ufw allow 58243/tcp
ufw status verbose
# Exit root
exit    
```

#### What to do when some cameras are not enumerating (Windows or Linux) (WTF does this mean - I couldn't connect via Ubuntu until I did this step)

[What to do when some cameras are not enumerating (Windows or Linux)](https://support.thinklucid.com/knowledgebase/some-of-my-cameras-are-not-enumerating/#)

Navigate to System -> System Settings -> Network

Select the IPv4 Settings tab, choose Manual for Method. In the Addresses heading, click Add and enter the following details:

| IP address | Subnet mask |
|---|---|
| 169.254.0.1 | 255.255.0.0 |

Click apply.

To set via terminal:

```sh
sudo ifconfig enp2s0 169.254.0.1 netmask 255.255.0.0
```

## Example test of SimulatedCamera

```py

import os
from openhsi.capture import *
from openhsi.cameras import *
import matplotlib.pyplot as plt

# Get the current working directory
CWD = os.getcwd()
ASSETS_FOLDER = os.path.join(CWD, "assets")
JSON_FILE = "OpenHSI-06_settings_Mono8_bin1.json"
PKL_FILE = "OpenHSI-06_calibration_Mono8_bin1.pkl"
json_path = os.path.join(ASSETS_FOLDER, JSON_FILE)
pkl_path = os.path.join(ASSETS_FOLDER, PKL_FILE)

IMG_FILE = "test_img.jpg"
TES_IMG = os.path.join(ASSETS_FOLDER, IMG_FILE)

with SimulatedCamera(
    n_lines=1024,
    processing_lvl=3,
    pkl_path=pkl_path,
    json_path=json_path,

) as cam:
    cam.collect()
    fig = cam.show(plot_lib="matplotlib", robust=True)

fig.opts(fig_inches=7,title="simulated hyperspectral datacube")

```

## Example test of LucidCamera

```py

import os
from openhsi.capture import *
from openhsi.cameras import *
import matplotlib.pyplot as plt

# Get the current working directory
CWD = os.getcwd()
ASSETS_FOLDER = os.path.join(CWD, "assets")
JSON_FILE = "OpenHSI-06_settings_Mono8_bin1.json"
PKL_FILE = "OpenHSI-06_calibration_Mono8_bin1.pkl"
json_path = os.path.join(ASSETS_FOLDER, JSON_FILE)
pkl_path = os.path.join(ASSETS_FOLDER, PKL_FILE)

with LucidCamera(n_lines        = 1000, 
                 processing_lvl = 2, 
                 pkl_path       = pkl_path,
                 json_path      = json_path,
                 exposure_ms    = 12
                ) as cam:
    cam.collect()
    fig = cam.show(plot_lib="matplotlib", robust=True)
     
fig

```

### Installing Py6S

[Py6S Instructions](https://py6s.readthedocs.io/en/latest/installation.html#installing-6s)

Install the 6S library:

```sh
mkdir source
mv ~/Downloads/6SV-1.1.tar source/
mkdir -p build/6SV/1.1
cd build
tar -xvf ../source/6SV-1.1.tar
cd 6SV1.1
sudo micro Makefile
```

Change the line:

```sh
FC      = g77 $(FFLAGS)
```

to:

```sh
FC      = gfortran -std=legacy -ffixed-line-length-none -ffpe-summary=none $(FFLAGS)
```

Save (ctrl + S) and quit (ctrl + Q).

Compile the source code:

```sh
make
```

Test the executable works:

```sh
# Note the guide has a missing "./" on Py6S
./sixsV1.1 < ../Examples/Example_In_1.txt
```

The output will look a bit like this:

```sh
*******************************************************************************
*                        atmospheric correction result                        *
*                        -----------------------------                        *
*       input apparent reflectance            :    0.100                      *
*       measured radiance [w/m2/sr/mic]       :   38.529                      *
*       atmospherically corrected reflectance                                 *
*       Lambertian case :      0.22187                                        *
*       BRDF       case :      0.22187                                        *
*       coefficients xa xb xc                 :  0.00685  0.03870  0.06820    *
*       y=xa*(measured radiance)-xb;  acr=y/(1.+xc*y)                         *
*******************************************************************************
```

Link 6S to a location on directory PATH:

```sh
sudo ln sixsV1.1 /usr/local/bin/sixs
```

Installing Py6S:

```sh
pip install Py6S
```

To test:

```sh
python3
from Py6S import *
SixS.test()
```

## How fast should I move the camera?

It’ll depend on what your case is. This answer assumes you want square pixels. Assuming the cross-track (scan line) spatial resolution is 0.42 mrad in the field of view, and your altitude is 120 m, the ground sample distance is:

```py
GSD =  0.00042  * 120   # Using the small angle approximation
GSD = 5              # (cm) 
```

Assuming your frame rate is 98 FPS at your desired processing level, and you want to get square pixels, you want to be flying at speed

```py
v = 98 * 0.05 = 4.9     # m/s
```

If you fly faster/slower than this, your datacube will appear to be stretched spatially.
