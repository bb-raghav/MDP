import os
import rasterio

raster_folder = "data/raw"

for file in os.listdir(raster_folder):

    if file.endswith(".tif"):

        path = os.path.join(raster_folder, file)

        with rasterio.open(path) as src:

            print("\n====================")
            print("File:", file)
            print("Shape:", src.shape)
            print("CRS:", src.crs)
            print("Bounds:", src.bounds)
            print("Resolution:", src.res)