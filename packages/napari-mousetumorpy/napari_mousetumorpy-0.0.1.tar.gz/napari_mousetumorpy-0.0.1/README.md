![EPFL Center for Imaging logo](https://imaging.epfl.ch/resources/logo-for-gitlab.svg)
# 🐭 napari-mousetumorpy

A Napari plugin for [mousetumorpy](https://github.com/EPFL-Center-for-Imaging/mousetumorpy.git): a toolbox to segment and track murine lung tumor nodules in mice CT scans.

## Installation

Install `napari-mousetumorpy` with `pip`:

```sh
pip install napari-mousetumorpy
```

or clone the project and install the development version:

```sh
git clone https://github.com/EPFL-Center-for-Imaging/napari-mousetumorpy.git
cd napari-mousetumorpy
pip install -e .
```

## Usage

Start napari from the terminal:

```sh
napari
```

You can find the plugin functions under `Plugins > Mousetumorpy`:

- `ROI and Lungs detection`: Segments the lungs and crops a CT scan around them.
- `Tumor segmentation`: Segments tumor nodules in a CT scan image (cropped around the lungs).
- `Track tumors`: Tracks tumor nodules in a 4D (TZYX) tumor segmentation masks series.

## Sample image

We provide a sample image under `File > Open Sample > Mouse lung CT scan` to test the package's functionality for lungs segmentation, cropping, and tumor segmentation.