# load libraries
import os
import xarray as xr
import rioxarray as rxr

def extract_and_resample(reference_folder, raster_folder):
    """
    Load a reference raster and reproject other rasters to match its resolution and CRS.
    Parameters:
        reference_path (str): Path to the reference raster (e.g., NDVI dataset).
        raster_paths (dict): Dictionary where keys are dataset names and values are paths to raster files.

    Returns:
        dict: Dictionary where keys are dataset names and values are reprojected raster datasets.
    """

    # Load reference dataset
    reference_path = os.path.join(reference_folder, "sentinel2_ndvi.tiff")
    reference_raster = rxr.open_rasterio(reference_path)

    # Get list of raster files in the raster folder
    raster_files = {
        os.path.splitext(file)[0]: os.path.join(raster_folder, file) 
        for file in os.listdir(raster_folder) if file.endswith(".tiff")
    }

    # Load and reproject other datasets
    # Load and reproject other datasets
    reprojected_rasters = {
        name: rxr.open_rasterio(path).rio.reproject_match(reference_raster)
        for name, path in raster_files.items()
    }

    return reference_raster, reprojected_rasters

# transform
def transform():
    reference_folder = "C:/Users/LOCATEG5/amini_technical_assignment/data/downloads/reference_data"
    raster_folder = "C:/Users/LOCATEG5/amini_technical_assignment/data/downloads/datasets_to_be_resampled"

    s2_ndvi, reprojected_rasters = extract_and_resample(reference_folder, raster_folder)

    # Extract individual datasets
    s1_vv = reprojected_rasters.get("sentinel1_vv")
    s1_vh = reprojected_rasters.get("sentinel1_vh")
    temperature = reprojected_rasters.get("temperature")
    elevation = reprojected_rasters.get("elevation")

    # Ensure all datasets have the same dimensions (width, height)
    if not (
        s1_vv.shape == s1_vh.shape == s2_ndvi.shape == temperature.shape == elevation.shape
    ):
        print("Warning: Some datasets may have mismatched dimensions!")

    # Check for missing values and fill with nearest pixel value
    datasets = [s1_vv, s1_vh, s2_ndvi, temperature, elevation]
    datasets = [ds.rio.interpolate_na(method="nearest") for ds in datasets]

    # Stack all rasters into a single multiband raster (concatenating along band dimension)
    multiband = xr.concat(datasets, dim="band")
    return multiband

# load to a local repository
def save_multiband():
    multiband = transform()
    multiband_saved = multiband.rio.to_raster("C:/Users/LOCATEG5/amini_technical_assignment/data/processed/test1/environmental_multiband_cog.tiff")
    print(f"Multiband created successfully 👏")
    return multiband

# # Use case
# save_multiband()