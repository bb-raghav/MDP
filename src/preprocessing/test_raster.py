import rasterio
import matplotlib.pyplot as plt

file_path = "data/raw/AER_Bengaluru.tif"

with rasterio.open(file_path) as src:
    data = src.read(1)

    print("Shape:", data.shape)
    print("CRS:", src.crs)
    print("Bounds:", src.bounds)

    plt.imshow(data)
    plt.colorbar()
    plt.title("AER Bengaluru")
    plt.show()