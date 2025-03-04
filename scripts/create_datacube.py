import xarray as xr
import os
from preprocess_data import extract_and_resample

def create_datacube():
    reference_folder = "C:/Users/LOCATEG5/amini_technical_assignment/data/downloads/reference_data"
    raster_folder = "C:/Users/LOCATEG5/amini_technical_assignment/data/downloads/datasets_to_be_resampled"
    
    s2_ndvi, reprojected_rasters = extract_and_resample(reference_folder, raster_folder)
    
    # Extract individual datasets
    s1_vv = reprojected_rasters.get("sentinel1_vv")
    s1_vh = reprojected_rasters.get("sentinel1_vh")
    temperature = reprojected_rasters.get("temperature")
    elevation = reprojected_rasters.get("elevation")

    # Check for missing values and fill with nearest pixel value
    datasets = [s1_vv, s1_vh, s2_ndvi, temperature, elevation]
    datasets = [ds.rio.interpolate_na(method="nearest") for ds in datasets]
    
    # Ensure all datasets have the same dimensions
    if not (datasets[0].shape == datasets[1].shape == datasets[2].shape == datasets[3].shape == datasets[4].shape):
        print("Warning: Some datasets may have mismatched dimensions!")
    
    # Assign CRS (EPSG:4326) to all datasets
    for ds in datasets:
        ds.rio.write_crs("EPSG:4326", inplace=True)
    
    # Stack rasters into an xarray DataArray (Band, Height, Width)
    datacube = xr.DataArray(
        data=[datasets[0][0], datasets[1][0], datasets[2][0], datasets[3][0], datasets[4][0]],
        dims=("band", "y", "x"),
        coords={
            "band": ["sentinel1_vv", "sentinel1_vh", "sentinel-2_ndvi", "temperature", "elevation"], 
            "y": s2_ndvi.y, 
            "x": s2_ndvi.x, 
        },
        attrs={
            "description": "Geospatial Datacube for Africa Environmental Land Monitoring @amini-africa-environmental-data-infrastructure 2025", 
            "crs": "EPSG:4326"
        }
    )
    
    # Convert to xarray Dataset
    datacube_ds = datacube.to_dataset(name="geospatial_datacube")
    
    # Assign spatial transform for correct georeferencing
    datacube_ds.rio.write_crs("EPSG:4326", inplace=True)
    datacube_ds.rio.set_spatial_dims(x_dim="x", y_dim="y", inplace=True)
    datacube_ds.rio.write_transform(s2_ndvi.rio.transform(), inplace=True)
    
    # Output file paths
    output_folder = "C:/Users/LOCATEG5/amini_technical_assignment/data/processed/test2"
    netcdf_path = os.path.join(output_folder, "africa_environmental_geospatial_datacube.nc")
    zarr_path = os.path.join(output_folder, "africa_environmental_geospatial_datacube.zarr")
    
    # Save as NetCDF
    datacube_ds.to_netcdf(netcdf_path)
    print(f"Datacube saved as NetCDF: {netcdf_path}")
    
    # Save as Zarr
    datacube_ds.to_zarr(zarr_path, mode="w")
    print(f"Datacube saved as Zarr: {zarr_path}")
    
    print("Geospatial Datacubes created successfully with 5 bands 👏")

# # Example usage
# create_datacube()