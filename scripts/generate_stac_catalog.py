import os
import pystac
import rasterio
from datetime import datetime
from shapely.geometry import box, mapping

def generate_stac_catalog():
    """
    Generate and save a STAC catalog for the environmental geospatial datacube.
    """
    # Define paths
    output_dir = "C:/Users/LOCATEG5/amini_technical_assignment/data/processed/test2"
    os.makedirs(output_dir, exist_ok=True)
    
    zarr_path = os.path.join(output_dir, "africa_environmental_geospatial_datacube.zarr")
    stac_json_path = os.path.join(output_dir, "stac_catalog")

    # Read spatial metadata from Zarr using Rasterio
    with rasterio.open(os.path.join(output_dir, "environmental_multiband_cog.tiff")) as src:
        bounds = src.bounds  # Get dataset extent
        bbox = [bounds.left, bounds.bottom, bounds.right, bounds.top]
        footprint = mapping(box(*bbox))  # Convert to GeoJSON polygon

    # Create a STAC Catalog
    catalog = pystac.Catalog(
        id="africa_environmental-datacube-catalog",
        description="STAC Catalog for Africa Environmental Data Infrastructure",
        catalog_type=pystac.CatalogType.SELF_CONTAINED
    )

    # Create a Collection
    collection = pystac.Collection(
        id="africa-environmental-datacube",
        description="Collection for Africa Environmental Data Infrastructure",
        extent=pystac.Extent(
            spatial=pystac.SpatialExtent([bbox]),
            temporal=pystac.TemporalExtent([[datetime.utcnow(), None]])
        ),
        license="CC-BY-4.0"
    )

    # Create a STAC Item
    item = pystac.Item(
        id="optimized_environmental_infrastructure-datacube",
        geometry=footprint,
        bbox=bbox,
        datetime=datetime.utcnow(),
        properties={"resolution": 10, "crs": "EPSG:4326"},
        collection=collection.id  # Associate item with collection
    )

    # Add Zarr file as an asset
    item.add_asset(
        "zarr",
        pystac.Asset(
            href=zarr_path,
            media_type="application/x-zarr",
            roles=["data"],
            title="Optimized Environmental Infrastructure Datacube"
        )
    )

    # Add collection to catalog
    catalog.add_child(collection)

    # Add item to collection
    collection.add_item(item)

    # Save STAC Catalog
    catalog.normalize_hrefs(stac_json_path)
    catalog.save(catalog_type=pystac.CatalogType.SELF_CONTAINED, dest_href=stac_json_path)

    print(f"STAC catalog successfully saved at: {stac_json_path}")

# Example usage
generate_stac_catalog()