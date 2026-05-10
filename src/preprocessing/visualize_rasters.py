import os
import rasterio
import matplotlib.pyplot as plt

folder = "data/raw"

for file in os.listdir(folder):

    if file.endswith(".tif"):

        path = os.path.join(folder, file)

        with rasterio.open(path) as src:

            data = src.read(1)

            plt.figure(figsize=(6, 6))
            plt.imshow(data)
            plt.colorbar()
            plt.title(file)

            plt.show()