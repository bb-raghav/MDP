import rasterio
import matplotlib.pyplot as plt
import numpy as np

from rasterio.enums import Resampling


def load_raster(path):

    with rasterio.open(path) as src:

        data = src.read(1)

        metadata = {
            "shape": src.shape,
            "crs": src.crs,
            "bounds": src.bounds,
            "resolution": src.res,
        }

    return data, metadata


def visualize_raster(data, title="Raster"):

    plt.figure(figsize=(6, 6))

    plt.imshow(data)

    plt.colorbar()

    plt.title(title)

    plt.show()


def resample_raster(path, target_height, target_width):

    with rasterio.open(path) as src:

        data = src.read(
            1,
            out_shape=(target_height, target_width),
            resampling=Resampling.bilinear
        )

    return data


def clean_array(data):

    data = np.where(
        np.isinf(data),
        np.nan,
        data
    )

    return data


def get_raster_metadata(path):

    with rasterio.open(path) as src:

        metadata = {
            "shape": src.shape,
            "crs": src.crs,
            "bounds": src.bounds,
            "resolution": src.res,
        }

    return metadata